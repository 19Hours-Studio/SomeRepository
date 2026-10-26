`solution.py` produces the correct digest (`5009dca8…`, which the scorer confirms matches the baseline), and my last self-check scored **32.7×** (2.22 s against roughly 73 s for the baseline). This machine is shared and the timings were noisy: CPU time on my own runs was about 1.6 s, so wall-clock time on a quiet machine should come out a bit lower.

**Approach:**
- **Bit-packing:** the grid is packed into 64-bit words, and each update is done with bitwise logic (adder-style circuits), so one numpy operation works on 64 cells at once.
- **Interleaved layout:** bit k of word w holds column k·64+w. A cell's left and right neighbours then sit in the adjacent words, so they are plain array slices with no shifting. Wrapping around the edges only needs one rotated pad word at each end of a row and one pad row above and below, rebuilt each step.
- **Counting the neighbours:** first a sideways sum (left+centre+right, and left+right), then a vertical add, all in a fixed sequence of 19 bitwise operations per block. The rule itself collapses to `alive = s1 & (s2 ^ (s0 | g))`, where s0, s1, s2 are the low bits of the neighbour count and g is the cell's current state. I also left out one adder output that's only needed where s1 is set.
- **Speed:**
  - Every array call works on a contiguous flat range. The row pads produce some wasted output, which gets overwritten before it's used.
  - The work runs in 128-row blocks, and the scratch buffers belong to one block (recomputing 2 overlap rows per block), so they stay in the L2 cache. Only the current and next grid move through main memory.
  - All array views are built once up front, so each step just runs through a ready-made list of about 600 numpy calls, using output arrays that already exist.

That brings a step to about 1.4 ms, against roughly 70 ms for the baseline.

Sources: none (no web searches were used).