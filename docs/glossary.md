# Glossary

Short, plain definitions of terms used in this project.

- **Connectome:** a wiring diagram of a nervous system: which neuron connects to which, and how many synapses. A static structure, not a running brain.
- **FlyWire:** the consortium and data set that produced the adult *Drosophila* whole-brain connectome (about 139,000 neurons, over 50 million synapses).
- **Neuron / synapse:** a neuron is a cell that integrates inputs and sends spikes. A synapse is a connection from one neuron to another.
- **Spike:** a brief electrical event a neuron emits when its membrane potential crosses a threshold.
- **Membrane potential (`v`):** the voltage across a neuron's membrane; the main state variable in the model.
- **Leaky integrate-and-fire (LIF):** a simple neuron model: the potential leaks toward rest, integrates input, and resets after a spike.
- **Firing rate:** spikes per second, usually estimated over a time window.
- **Excitatory / inhibitory:** an excitatory synapse pushes the target toward spiking, an inhibitory one pushes it away. In the FlyWire-based model the sign comes from the predicted neurotransmitter.
- **Sensory neuron:** brings information in from the body (smell, light, touch, ...).
- **Descending neuron:** carries commands from the brain down to the nerve cord (the "spinal cord" analogue), which drives the legs and wings. We use these as the brain's output signal.
- **Motor neuron:** drives muscles.
- **Reservoir computing:** a method where a fixed, rich recurrent network transforms inputs and only a simple readout layer is trained. Here the connectome is the fixed reservoir.
- **Readout layer:** the trainable linear map from selected neuron activity to the motor command.
- **Ridge regression:** least-squares fitting with a penalty on weight size, used to train the readout in one step.
- **Plasticity:** change of synaptic strengths over time (learning). Not part of the connectome data; out of scope until after v1.0.
- **Hardware-in-the-loop:** testing where the real hardware is connected to the simulation in a closed loop.
- **Rheobase:** the smallest constant input current that makes a neuron spike.
