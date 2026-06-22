"""Parameter validation utilities."""
from typing import Optional, Tuple


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_quality(quality: int) -> Tuple[bool, Optional[str]]:
    """
    Validate quality parameter.
    
    Args:
        quality: Quality value to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(quality, int):
        return False, "Quality must be an integer"
    if quality < 1 or quality > 100:
        return False, "Quality must be between 1 and 100"
    return True, None


def validate_dimensions(
    width: Optional[int],
    height: Optional[int],
    format: str = "webp"
) -> Tuple[bool, Optional[str]]:
    """
    Validate image dimensions.
    
    Args:
        width: Maximum width
        height: Maximum height
        format: Output format
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # WebP has a maximum dimension limit
    webp_max = 16383
    
    if format.lower() == "webp":
        if width and width > webp_max:
            return False, f"WebP format has a maximum width of {webp_max} pixels"
        if height and height > webp_max:
            return False, f"WebP format has a maximum height of {webp_max} pixels"
            
    if width and width < 1:
        return False, "Width must be greater than 0"
    if height and height < 1:
        return False, "Height must be greater than 0"
        
    return True, None


def validate_tile_size(tile_size: int) -> Tuple[bool, Optional[str]]:
    """
    Validate tile size parameter.
    
    Args:
        tile_size: Tile size to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(tile_size, int):
        return False, "Tile size must be an integer"
    if tile_size < 128:
        return False, "Tile size should be at least 128 pixels"
    if tile_size > 4096:
        return False, "Tile size should not exceed 4096 pixels"
    
    # Check if it's a power of 2 (recommended but not required)
    if tile_size & (tile_size - 1) != 0:
        return True, "Warning: Tile size is not a power of 2 (e.g., 256, 512, 1024)"
        
    return True, None


def validate_target_size(target_size: int) -> Tuple[bool, Optional[str]]:
    """
    Validate target file size.
    
    Args:
        target_size: Target size in bytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(target_size, int):
        return False, "Target size must be an integer"
    if target_size < 1024:
        return False, "Target size should be at least 1KB (1024 bytes)"
    if target_size > 100 * 1024 * 1024:
        return False, "Target size seems too large (>100MB)"
        
    return True, None


def validate_jobs(jobs: int) -> Tuple[bool, Optional[str]]:
    """
    Validate number of parallel jobs.
    
    Args:
        jobs: Number of jobs
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(jobs, int):
        return False, "Jobs must be an integer"
    if jobs < 1:
        return False, "Jobs must be at least 1"
    if jobs > 32:
        return False, "Jobs should not exceed 32"
        
    return True, None


def validate_file_path(path: str, must_exist: bool = True) -> Tuple[bool, Optional[str]]:
    """
    Validate file path.
    
    Args:
        path: File path to validate
        must_exist: Whether the file must exist
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    import os
    
    if not path:
        return False, "Path cannot be empty"
        
    if must_exist and not os.path.exists(path):
        return False, f"Path does not exist: {path}"
        
    if must_exist and not os.path.isfile(path):
        return False, f"Path is not a file: {path}"
        
    return True, None


def validate_directory_path(path: str, must_exist: bool = True) -> Tuple[bool, Optional[str]]:
    """
    Validate directory path.
    
    Args:
        path: Directory path to validate
        must_exist: Whether the directory must exist
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    import os
    
    if not path:
        return False, "Path cannot be empty"
        
    if must_exist and not os.path.exists(path):
        return False, f"Directory does not exist: {path}"
        
    if must_exist and not os.path.isdir(path):
        return False, f"Path is not a directory: {path}"
        
    return True, None
