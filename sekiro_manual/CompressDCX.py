import zlib
import struct

def compress_dcx_content(param):
    HEADER_LENGTH = 0x2c
    COMP_HEADER_LENGTH = 0x08
    
    uncomp_size = len(param)
    comp_obj = zlib.compressobj(level = 9, wbits = -15)
    compressed_data = comp_obj.compress(param)
    compressed_data += comp_obj.flush()
    comp_size = len(compressed_data) + 2 # Add two to include the \x78\xDA bytes.
    
    return_data = b"DCX\x00" 
    return_data += struct.pack("<I", 0x100) 
    return_data += struct.pack(">III", 0x18, 0x24, 0x24)
    return_data += struct.pack(">I", HEADER_LENGTH)
    return_data += b"DCS\x00"
    return_data += struct.pack(">II", uncomp_size, comp_size)
    return_data += b"DCP\x00DFLT"
    # Begin unknown header portion
    return_data += struct.pack(">I", 0x20)
    return_data += struct.pack("<IIII", 0x09, 0x00, 0x00, 0x00)
    return_data += b"\x00\x01\x01\x00"
    # End unknown header portion
    return_data += b"DCA\x00"
    return_data += struct.pack(">I", COMP_HEADER_LENGTH)
    return_data += b"\x78\xDA"
    return_data += compressed_data
    # Add checksum to file (not strictly needed in DS1, but .dcx includes this).
    return_data += struct.pack(">I", zlib.adler32(param))
    return(return_data)
