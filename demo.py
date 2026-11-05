"""Demonstration of the Assignment 2 smart-energy event pipeline."""
from stream_framework import ActiveMeterFilter, EnergyEvent, EnergyMetricsTransformer


def main() -> None:
    events = [
        EnergyEvent("HVAC-01", "HVAC", 6.2, 1.4, True),
        EnergyEvent("SOLAR-02", "solar_inverter", 0.03, 0.02, True),
        EnergyEvent("BAT-03", "battery_storage", 2.1, 0.8, False),
        EnergyEvent("HVAC-04", "HVAC", 5.4, 1.1, True),
    ]
    pipeline = ActiveMeterFilter(0.1) | EnergyMetricsTransformer(
        carbon_kg_per_kwh=0.35, peak_tariff_threshold_kw=5.0, baseline_load_kw=2.0
    )
    print("Streaming results:")
    for result in pipeline.run(events):
        print(f"{result.meter_id} ({result.device_type}) | load balance: "
              f"{result.load_balance_kw:.2f} kW | carbon: "
              f"{result.carbon_kg_co2e:.3f} kg CO2e | peak tariff: {result.peak_tariff}")

    iterator_pipeline = (ActiveMeterFilter(0.1) | EnergyMetricsTransformer()).from_iterable(events)
    stream = iter(iterator_pipeline)
    print("\nFirst result obtained with next():")
    try:
        print(next(stream))
    except StopIteration:
        print("No valid events")


if __name__ == "__main__":
    main()
