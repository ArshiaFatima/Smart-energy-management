import unittest
from stream_framework import (ActiveMeterFilter, EnergyEvent, EnergyMetricsTransformer,
                              Pipeline, ProcessedEnergyEvent, StreamProcessor)


class StreamFrameworkTests(unittest.TestCase):
    def setUp(self):
        self.events = [
            EnergyEvent("M1", "HVAC", 6.0, 2.0, True),
            EnergyEvent("M2", "solar_inverter", 0.01, 0.01, True),
            EnergyEvent("M3", "battery_storage", 4.0, 1.0, False),
        ]

    def test_abstract_base_class_contract(self):
        with self.assertRaises(TypeError):
            StreamProcessor()

    def test_filter_drops_inactive_and_subthreshold_events(self):
        processor = ActiveMeterFilter(0.1)
        self.assertIsNotNone(processor.process(self.events[0]))
        self.assertIsNone(processor.process(self.events[1]))
        self.assertIsNone(processor.process(self.events[2]))

    def test_transformer_calculates_metrics(self):
        result = EnergyMetricsTransformer(0.5, 5.0, 2.0).process(self.events[0])
        self.assertIsInstance(result, ProcessedEnergyEvent)
        self.assertEqual(result.load_balance_kw, 4.0)
        self.assertEqual(result.carbon_kg_co2e, 1.0)
        self.assertTrue(result.peak_tariff)

    def test_operator_overloading_and_pipeline(self):
        pipeline = ActiveMeterFilter(0.1) | EnergyMetricsTransformer()
        self.assertIsInstance(pipeline, Pipeline)
        self.assertEqual(len(list(pipeline.run(self.events))), 1)

    def test_iterator_protocol(self):
        pipeline = (ActiveMeterFilter(0.1) | EnergyMetricsTransformer()).from_iterable(self.events)
        first = next(iter(pipeline))
        self.assertEqual(first.meter_id, "M1")


if __name__ == "__main__":
    unittest.main()
