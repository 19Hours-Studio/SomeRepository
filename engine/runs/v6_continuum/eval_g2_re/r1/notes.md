I1: need 44TB/s/(51.2GB*8)=107 GB/s/Gb; Alibaba 1.38TB/s over 602mm2*64Mb/mm2=38.5Gb -> 35.8 GB/s/Gb (capacity unpublished; 135 unverified). margin 0.33
I2: 1.5x needs pkg<=0.259*45k=$11.7k; HBM 288GB*$16=$4.6k +1.5k+2k=$8.1k -> 1.44 (idea's $16k -> 0.73)
I3: 1000 tok/s over 17 stages => 2.25us/all-reduce; avail ~32us NCCL small allreduce on 8xB300 NVLink (arXiv 2603.11438), no 32-die organic data
I4: 39.7GB/0.864TB/s=46ms => 21.8 tok/s/user vs 100
I5: 1.5x needs $14.3k pkg vs $55k; HBM saving 96GB*18.4=$1.8k
I6: need 27.6TB/s/1600mm2=17.25 GB/s/mm2; Alibaba 1.38TB/s/602mm2=2.29
