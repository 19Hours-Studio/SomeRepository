# Seed (known family): 2-layer unidirectional GRU (reads the data, then answers at the blanks).
class Model(nn.Module):
    def __init__(self, vocab_size, max_len, d=96):
        super().__init__(); self.emb = nn.Embedding(vocab_size, d); self.rnn = nn.GRU(d, d, num_layers=2, batch_first=True)
        self.out = nn.Linear(d, vocab_size)
    def forward(self, x):
        return self.out(self.rnn(self.emb(x))[0])
