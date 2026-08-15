import torch
import torch.nn as nn
import snntorch as snn
from gvf_core import GVFFieldGenerator

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class GVF_SNN(nn.Module):
    def __init__(self, num_inputs=2*34*34, num_hidden=128, num_outputs=10):
        super().__init__()
        self.fc1 = nn.Linear(num_inputs, num_hidden)
        self.lif1 = snn.Leaky(beta=0.9, threshold=1.0)
        self.fc2 = nn.Linear(num_hidden, num_outputs)
        self.lif2 = snn.Leaky(beta=0.9, threshold=1.0)

    def forward(self, x, gvf_generator):
        mem1 = self.lif1.init_leaky()
        mem2 = self.lif2.init_leaky()
        spk2_rec = []
        for step in range(x.shape[0]):
            current_vth = gvf_generator.get_threshold(step)
            self.lif1.threshold = current_vth
            self.lif2.threshold = current_vth
            cur1 = self.fc1(x[step].flatten(1))
            spk1, mem1 = self.lif1(cur1, mem1)
            cur2 = self.fc2(spk1)
            spk2, mem2 = self.lif2(cur2, mem2)
            spk2_rec.append(spk2)
        return torch.stack(spk2_rec, dim=0)

if __name__ == "__main__":
    print("GVF SNN Pipeline Loaded Successfully.")
