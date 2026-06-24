import numpy as np
from datetime import datetime, timezone
from uuid import uuid4

from pynwb import NWBFile, NWBHDF5IO, TimeSeries
from pynwb.file import Subject
from pynwb.ecephys import ElectricalSeries, LFP
from pynwb.behavior import BehavioralTimeSeries



rng = np.random.default_rng(0)

nwb_setup = NWBFile(
    session_description="Synthetic ephys session for course exercises",
    identifier=str(uuid4()),
    session_start_time=datetime(2026, 5, 1, 10, 0, 0, tzinfo=timezone.utc),
    experimenter="Dr. Demo",
    lab="Anda Demo Lab",
    institution="Demo University",
    session_id="demo-001",
)
nwb_setup.subject = Subject(
    subject_id="mouse-01", species="Mus musculus", sex="M", age="P60D",
    description="Synthetic subject for the course",
)

device = nwb_setup.create_device(name="probe-A", description="Synthetic 8-channel probe")
group_v1 = nwb_setup.create_electrode_group(
    name="shank-V1", description="Channels in V1", location="V1", device=device,
)
group_hpc = nwb_setup.create_electrode_group(
    name="shank-HPC", description="Channels in hippocampus", location="HPC", device=device,
)
for i in range(4):
    nwb_setup.add_electrode(x=float(i), y=0.0, z=0.0, location="V1",
                            group=group_v1, filtering="none")
for i in range(4):
    nwb_setup.add_electrode(x=float(i), y=100.0, z=0.0, location="HPC",
                            group=group_hpc, filtering="none")

electrode_region = nwb_setup.create_electrode_table_region(
    region=list(range(8)), description="All electrodes"
)

raw_signal = rng.standard_normal((5000, 8)).astype("float32") * 50e-6  # in volts
nwb_setup.add_acquisition(ElectricalSeries(
    name="ElectricalSeries", data=raw_signal, electrodes=electrode_region,
    rate=1000.0, starting_time=0.0,
))

lfp_signal = raw_signal[::4, :].copy()
lfp = LFP(electrical_series=ElectricalSeries(
    name="lfp", data=lfp_signal, electrodes=electrode_region,
    rate=250.0, starting_time=0.0,
))
ecephys = nwb_setup.create_processing_module(name="ecephys", description="Derived ecephys")
ecephys.add(lfp)

# --- Behavioural variables --------------------------------------------------
# 5 seconds of behaviour sampled at 50 Hz (250 samples), matching the ephys.
behavior_rate = 50.0
n_behavior = 250
t_behavior = np.arange(n_behavior) / behavior_rate

# Running speed (cm/s): a smooth drifting baseline plus noise, clipped at 0 so
# the mouse never runs "backwards". Two brief bouts of running are added.
running_speed = (
    5.0
    + 3.0 * np.sin(2 * np.pi * 0.2 * t_behavior)
    + rng.standard_normal(n_behavior) * 1.0
)
running_speed[(t_behavior > 1.0) & (t_behavior < 1.8)] += 15.0
running_speed[(t_behavior > 3.5) & (t_behavior < 4.2)] += 20.0
running_speed = np.clip(running_speed, 0.0, None).astype("float32")

# Pupil diameter (mm): slow fluctuations that loosely track arousal/running.
pupil_diameter = (
    1.2
    + 0.15 * np.sin(2 * np.pi * 0.15 * t_behavior + 0.5)
    + 0.005 * running_speed
    + rng.standard_normal(n_behavior) * 0.02
).astype("float32")

behavior = nwb_setup.create_processing_module(
    name="behavior", description="Behavioural variables"
)
behavior.add(BehavioralTimeSeries(
    name="BehavioralTimeSeries",
    time_series=[
        TimeSeries(
            name="running_speed", data=running_speed, unit="cm/s",
            rate=behavior_rate, starting_time=0.0,
            description="Treadmill running speed",
        ),
        TimeSeries(
            name="pupil_diameter", data=pupil_diameter, unit="mm",
            rate=behavior_rate, starting_time=0.0,
            description="Pupil diameter from eye tracking",
        ),
    ],
))

nwb_setup.add_trial_column(name="stim_type", description="Stimulus identifier")
for i in range(10):
    nwb_setup.add_trial(start_time=i * 0.5, stop_time=i * 0.5 + 0.3,
                        stim_type=("A" if i % 2 == 0 else "B"))

for n in (20, 35, 12):
    nwb_setup.add_unit(spike_times=np.sort(rng.uniform(0, 5, size=n)))

with NWBHDF5IO("synthetic_session.nwb", "w") as io:
    io.write(nwb_setup)
print("Wrote synthetic_session.nwb")