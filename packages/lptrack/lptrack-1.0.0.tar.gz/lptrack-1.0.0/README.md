# LPTrack

LavaPlayer encoded track encoder and decoder.


## Introduction

LPTrack is a small library which allows you to interpret the encoded
track data used by LavaPlayer.

This is useful when you're dealing with standalone LavaLink instances
like [Lavalink](https://github.com/Frederikam/Lavalink) and [Andesite](https://github.com/natanbc/andesite-node),
because it allows you to interpret the track data directly.


## Installation

#### From PyPI

```shell
pip install lptrack
```


## Usage

```python
import lptrack

track = lptrack.Track(
    version = 2,
    source = lptrack.Youtube(),

    info = lptrack.TrackInfo(
        title="A song",
        author="Some random artist",
        duration=120,                   # duration is in seconds!
        identifier="dQw4w9WgXcQ",
        is_stream=False,
    ),
)

encoded = lptrack.encode(track)
print(encoded)
# b'QAAARQIABkEgc29uZwASU29tZSByYW5kb20gYXJ0aXN0AAAAAAAB1MAAC2RRdzR3OVdnWGNRAAAAB3lvdXR1YmUAAAAAAAAAAA=='

decoded = lptrack.decode(encoded)

assert decoded == encoded
```

## Obligatory rant about CESU-8

Without going into too much detail, LavaPlayer (or Java, to be more
specific) uses a special encoding for strings called [MUTF-8](https://en.wikipedia.org/wiki/UTF-8#Modified_UTF-8)
which in turn is based on [CESU-8](https://en.wikipedia.org/wiki/CESU-8).
Characters from the [BMP](https://github.com/LuminosoInsight/python-ftfy)
(which contains pretty much all characters from modern languages) are
encoded like normal UTF-8. But special characters like
emojis will be encoded in an incompatible manner.

While lptrack doesn't force you to use it, it's strongly recommended to
have [ftfy](https://github.com/LuminosoInsight/python-ftfy) installed.
It allows lptrack to properly decode MUTF-8 encoded strings. If ftfy
isn't installed lptrack will treat the strings as UTF-8, but allows
surrogates. Note that it doesn't parse the surrogates properly (i.e. it
will look like a mess), but it will include them in the re-encoded track
data.

ftfy is listed as a dependency of lptrack, so unless you really don't
want it, you'll enjoy its benefits.

lptrack itself doesn't produce CESU-8 strings, so it's possible that
the re-encoded track data differs from the original track data.

It's possible to manually set the desired codec using the
keyword-argument `string_codec` which accepts a `lptrack.strcodec.Codec`
instance. The following values are pre-defined:

- `lptrack.strcodec.UTF8`: Allows surrogates but doesn't parse them
    properly. Should be used if re-encoded track data needs to be equal
    to the input.

- `lptrack.strcodec.MUTF8`: Codec handling CESU-8. Requires ftfy to
    work.

- `lptrack.strcodec.DEFAULT`: MUTF8 if ftfy is installed, UTF8 otherwise.
    This codec is used by default.

- `lptrack.strcodec.UTF8STRICT`: Same as UTF8 but rejects surrogates
    outright.

