# [photofind](https://github.com/rstms/photofind)

A `find` workalike for scanning directories detecting image files, reading and filtering selected EXIF data tags.

## geolocation filter
The --distance filters image files based on the distance between the given GPS coordinates and the EXIF GPS data in the scanned image files.

## command line 
```
Usage: photofind [OPTIONS] [DIRECTORY]

  Scan DIRECTORY for image files, printing filenames and selected EXIF data

Options:
  -r, --recurse              descend into subdirectories
  -f, --file_filter TEXT     regex pattern to select filenames
  -t, --include_filter TEXT  regex pattern to select EXIF tags (default is
                             all)
  -T, --exclude_filter TEXT  regex pattern to exclude EXIF tags (default is
                             '.*[tT]humbnail.*|EXIF MakerNote|Filename' use
                             '\.^' to exclude nothing
  -j, --format-json          output as JSON
  -c, --compact              compact output
  -n, --no_exif              output only files with no EXIF data
  -d, --distance TEXT        filter output by distance given
                             LATITUDE,LONGITUDE,METERS in decimal
                             (include_filter must include GPS data
  --data / --no-data         output EXIF data
  --help                     Show this message and exit.
```
