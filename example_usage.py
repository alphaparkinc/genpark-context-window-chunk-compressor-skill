from client import ContextChunkCompressor

ctx = "The sky is clear today. Distributed databases rely on Raft consensus for fault tolerance. Coffee beans require grinding. Raft ensures state machine logs are consistently replicated."
query = "Explain Raft consensus fault tolerance."

compressed = ContextChunkCompressor.compress(ctx, query, max_chars=160)
print(f"Original Length: {len(ctx)} chars")
print(f"Compressed Output: {compressed}")
