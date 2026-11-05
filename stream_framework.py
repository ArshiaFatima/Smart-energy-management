"""Reusable OOP stream-processing framework for smart-energy events."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable, Iterator, Optional


@dataclass
class EnergyEvent:
    """Raw event received from an IoT smart meter."""
    meter_id: str
    device_type: str
    power_kw: float
    energy_kwh: float
    active: bool = True
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not self.meter_id.strip():
            raise ValueError("meter_id cannot be empty")
        if self.power_kw < 0 or self.energy_kwh < 0:
            raise ValueError("power_kw and energy_kwh cannot be negative")


@dataclass
class ProcessedEnergyEvent:
    """Enriched event emitted by the processing pipeline."""
    meter_id: str
    device_type: str
    power_kw: float
    energy_kwh: float
    load_balance_kw: float
    carbon_kg_co2e: float
    peak_tariff: bool
    timestamp: datetime


class StreamProcessor(ABC):
    """Abstract contract: every processor must implement process()."""

    @abstractmethod
    def process(self, event: Any) -> Optional[Any]:
        """Process one event; return None when the event should be discarded."""
        raise NotImplementedError

    def __or__(self, other: "StreamProcessor") -> "Pipeline":
        """Allow processors to be composed with the | operator."""
        if isinstance(self, Pipeline):
            return Pipeline([*self.processors, other])
        return Pipeline([self, other])


class Pipeline(StreamProcessor):
    """Executes processors sequentially and exposes generator/iterator APIs."""

    def __init__(self, processors: Iterable[StreamProcessor]) -> None:
        self.processors = list(processors)
        if not self.processors:
            raise ValueError("A pipeline needs at least one processor")

    def process(self, event: Any) -> Optional[Any]:
        current = event
        for processor in self.processors:
            if current is None:
                return None
            current = processor.process(current)
        return current

    def __or__(self, other: StreamProcessor) -> "Pipeline":
        return Pipeline([*self.processors, other])

    def run(self, events: Iterable[Any]) -> Iterator[Any]:
        """Generator: consume source events and yield non-discarded results."""
        for event in events:
            result = self.process(event)
            if result is not None:
                yield result

    def from_iterable(self, events: Iterable[Any]) -> "Pipeline":
        """Attach an iterable source so the pipeline can be used with next()."""
        self._source = events
        return self

    def __iter__(self) -> "Pipeline":
        if not hasattr(self, "_source"):
            raise RuntimeError("Call from_iterable(events) before iterating")
        self._iterator = self.run(self._source)
        return self

    def __next__(self) -> Any:
        if not hasattr(self, "_iterator"):
            self.__iter__()
        return next(self._iterator)


class ActiveMeterFilter(StreamProcessor):
    """Filters inactive meters and readings below a configured power threshold."""

    def __init__(self, min_power_kw: float = 0.1) -> None:
        self.min_power_kw = min_power_kw

    @property
    def min_power_kw(self) -> float:
        return self._min_power_kw

    @min_power_kw.setter
    def min_power_kw(self, value: float) -> None:
        if value < 0:
            raise ValueError("min_power_kw cannot be negative")
        self._min_power_kw = value

    def process(self, event: EnergyEvent) -> Optional[EnergyEvent]:
        if not event.active or event.power_kw < self.min_power_kw:
            return None
        return event


class EnergyMetricsTransformer(StreamProcessor):
    """Calculates load balance, carbon equivalent, and peak-tariff status."""

    def __init__(self, carbon_kg_per_kwh: float = 0.35,
                 peak_tariff_threshold_kw: float = 5.0,
                 baseline_load_kw: float = 0.0) -> None:
        if carbon_kg_per_kwh < 0 or peak_tariff_threshold_kw < 0:
            raise ValueError("Carbon factor and tariff threshold cannot be negative")
        self.carbon_kg_per_kwh = carbon_kg_per_kwh
        self.peak_tariff_threshold_kw = peak_tariff_threshold_kw
        self.baseline_load_kw = baseline_load_kw

    def process(self, event: EnergyEvent) -> ProcessedEnergyEvent:
        return ProcessedEnergyEvent(
            meter_id=event.meter_id,
            device_type=event.device_type,
            power_kw=event.power_kw,
            energy_kwh=event.energy_kwh,
            load_balance_kw=round(event.power_kw - self.baseline_load_kw, 3),
            carbon_kg_co2e=round(event.energy_kwh * self.carbon_kg_per_kwh, 3),
            peak_tariff=event.power_kw >= self.peak_tariff_threshold_kw,
            timestamp=event.timestamp,
        )


class EventCounter(StreamProcessor):
    """Optional processor showing that different classes share one API."""

    def __init__(self) -> None:
        self.processed_count = 0

    def process(self, event: Any) -> Any:
        self.processed_count += 1
        return event
