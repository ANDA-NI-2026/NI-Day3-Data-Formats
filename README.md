# NI Day 3: Data Formats and Storage for Electrophysiology with HDF5 and NWB

## Staff

 - **Lead Trainer**:
   - Atle E. Rimehaug, Uni Bonn, Germany
 - **Lecturers**: 
   - Atle E. Rimehaug, Uni Bonn, Germany
 - **Teaching Assistants**: 
    - Ole Bialas, Uni Bonn, Germany
    - Julio Rodino, Forchungszentrum Jülich, Germany
    - Junji Ito, Forchungszentrum Jülich, Germany 

## Session Overview

How do we store an electrophysiology recording so that someone else — or our
future selves — can open it months later and still know what every array means,
how it was sampled, and where it came from?

In these sessions, you will work with the data formats that underpin
modern neurophysiology: [HDF5](https://www.hdfgroup.org/solutions/hdf5/), the
general-purpose hierarchical container, and
[Neurodata Without Borders (NWB)](https://www.nwb.org/), the neuroscience community standard
built on top of it.

In the homework, you will with the HDF5 format itself, using the `h5py` library to write
mixed-type, labelled data and metadata into structured files and to read data back
selectively without loading everything into memory. 

In the in-class sessions, we will turn to NWB and see that an NWB file is *just HDF5 with a schema*. NWB files can be opened and inspected with both `h5py` and `pynwb` but to work with the typed objects - data objects with information about what the data represents included - that a NWB file contains, you will use `pynwb`.

Finally, you will learn how to build an NWB file from scratch with `pynwb` — adding session
and subject metadata, registering recording devices and an electrode table,
storing raw acquisition alongside processed data such as LFP and behavioural
signals, and writing trial and unit tables.

The rest of the day's materials, including exercises, notebooks, datasets, and solutions will appear in this repo during the session. Just call `git pull` and you'll get the updates.

See you there!
