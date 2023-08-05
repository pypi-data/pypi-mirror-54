from .test_verify import *

# This test file runs normally after test_verify.  We only clean up the .c
# sources, to check that it also works when we have only the .so.  The
# tests should run much faster than test_verify.

def setup_module():
    import cffi.verifier
    cffi.verifier.cleanup_tmpdir(keep_so=True)
