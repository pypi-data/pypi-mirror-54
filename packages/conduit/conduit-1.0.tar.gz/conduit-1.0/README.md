# Conduit

[![Build Status](https://travis-ci.com/PingThingsIO/conduit.svg?token=5gAjQxGQg8bpYHKH9FmB&branch=develop)](https://travis-ci.com/PingThingsIO/conduit)
[![codecov](https://codecov.io/gh/PingThingsIO/conduit/branch/develop/graph/badge.svg?token=0H80nr9jut)](https://codecov.io/gh/PingThingsIO/conduit)
![PyPI](https://img.shields.io/pypi/v/conduit.svg)

**Python stream transformation package for common Power Engineering analytics.**

## Data Model

A conduit wraps a stream set and can contain one or more streams. Functions can be applied to a conduit to create a data flow that:

1. Produces a `DataFrame` on demand
2. Ensures data is aligned with time index
3. Ensures that correct streams are selected for computation

On demand `DataFrame` means that a user only has to configure a conduit and can then get computed data on demand from those streams, e.g. different time windows. Note that conduit should also support selecting aggregates with aligned windows or windows for higher levels of granularity. This requirement really is to minimize the amount of memory/duplicated arrays created by computation in a notebook.

Time alignment is also critical to ensure that streams are measured at the same time periods. If there is missing data, these should be `np.nan` and all streams should have the same time index. This alignment protects from issues in downstream computations.

Certain computations only apply to particular stream types or to groups of streams. These must be validated ahead of time. The following data structures are considered:

- **Streams**: the simplest validator, this ensures a computation works for a stream, e.g, radians can only be computed from degrees, or line to neutral is only computed from a voltage magnitude.
- **Phasors**: requires angle and magnitude, either voltage or current
- **Phasor pair**: voltage and current phasors for a specific phase
- **Phasor group**: either voltage or current phasors for all phases
- **Phasor pair group**: phasor pairs for all three phasors

The question for conduit is really about how to create these groups semiautomatically and to pass streams through the various computations required.

Should the order of streams in the stream set be preserved? E.g. should we have an index mechanism or mapping mechanism for use in transformations?

## Transformations

Most computations operate on a series or data frame object. They do need to know which streams are which and do require some metadata.

Do we decouple transformations from conduit to allow them to be used generically?

Consider the following typical dataflow computation:

![Symmetric Components Dataflow](docs/source/_static/dataflow.png)

How do we easily define this dataflow with functional components ensuring that the intermediate objects and data structures (as described above) are validated and maintained?

## Open Questions

1. Is VPHM always Volts? Can it be Volts_L_L or Volts_L_N?
2. Should we always validate the phase is the same in phasors or leave it to the user?