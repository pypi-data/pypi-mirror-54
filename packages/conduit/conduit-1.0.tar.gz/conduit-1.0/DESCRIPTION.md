# Conduit

**Python stream transformation package for common Power Engineering analytics.**

Conduit integrates with [btrdb-python](https://btrdb.readthedocs.io/en/latest/) to support a series of common power engineering analytics on synchrophasor data queried from a BTrDB database. These transformations are applied to Pandas Series and DataFrame objects that have been materialized through database queries alongside the tags and annotations that provide metadata for each stream. Currently the following transformations are implemented:

**Conversions**

- Per Unit
- Line to Line
- Line to Neutral
- Amps
- Calibrate
- Radians
- Degrees

**Phasor**

- Real
- Imaginary
- Complex Phasor

**Phasor Pair**

- Complex Power (P + jQ)
- Real Power (P)
- Reactive Power (Q)
- Apparent Power (S)
- Power Factor

**Phasor Group**

- Complex Phasor Group
- Sequence Components
- Zero Sequence
- Positive Sequence
- Negative Sequence

## Notes

For users of conduit v0.0.8 or earlier, a framework for dataflow-style python programming, the versions are still maintained here. Starting with version 1.0 the new conduit package is a power engineering analytics library that also has dataflow-like properties. We would like to say a special thank you to [@sleibman](https://github.com/sleibman) for allowing us to take over this namespace for our project!