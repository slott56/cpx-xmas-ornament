"""
xmas_ornament.py

1. Red Green LED dance.
2. Music.

See http://www.sengpielaudio.com/calculator-notenames.htm for
scientific note notation.

https://en.wikipedia.org/wiki/Music_Macro_Language

https://visionshome.guildlaunch.com/forums/viewtopic.php?t=11312319

https://archeagemmllibrary.com/we-wish-you-a-merry-christmas/

# T tempo (default t120, 120 quarter notes/sec)
# l length (l5 = quarter notes)
# V volume (V15 -- full blast)
# o octave (o4)
# < and > decrease and increase octave
# p (or r) pause (or rest)
# a-g pitch
# Durations are 1, 2, 4, 8, etc. with optional "." and optional "&"
# n is a specific note number (0 to 127) n0 == c0 up to n96 or so.
"""

import time
from adafruit_circuitplayground.express import cpx
import random

# TODO: include '#', '♯', '♭'
step_names = {
        "c-": -1,  # Odd, but seen in the wild.
    "c": 0,
        "c+": 1, "d-": 1,
    "d": 2,
        "d+": 3, "e-": 3,
    "e": 4,
    "f": 5,
        "f+": 6, "g-": 6,
    "g": 7,
        "g+": 8, "a-": 8,
    "a": 9,
        "a+": 10, "b-": 10,
    "b": 11,
        "b+": 12,  # Also odd, but.
}
factor = 2**(1/12)
A4 = 57
def fq(octave, step):
    """Octave 0 is threshold of hearing.
    >>> fq("c", 0)
    16
    >>> fq("a", 0)
    27.5
    >>> fq("a", 4)
    440
    """
    return 440.0 * factor ** (step+octave*12 - A4)

# Note is a 3-tuple of fq, duration, volume.

def fq_iter(text):
    context = {"T": 120, "l": 5, "V": 15, "o": 4}
    i = 0
    while i != len(text):
        c = text[i]  # Character
        if i+1 != len(text) and text[i+1] in {'+', '-', '#', '♯', '♭'}:  # Optional modifier
            i += 1
            c += text[i]
        n = 0   # Optional number after letter
        while i+1 != len(text) and text[i+1].isdigit():
            i = i + 1
            n = 10*n + int(text[i])
        dots = ''  # Optional dot(s) after number
        while i+1 != len(text) and text[i+1] == '.':
            i = i + 1
            dots += '.'
        if dots:
            # "." = +1/2. In principle ".."  = +3/4, but it's not supported.
            # f = 2**len(dots); n += n*(f-1)//f
            n += n // 2
        if i+1 != len(text) and text[i+1] == '&':  # Optional no-gap modifier
            i += 1
        # Done with this note's codes.
        i += 1
        # Interpret the code, c
        if c.isspace() or c == ',' or c == ';':
            continue
        elif c in context:
            context[c] = n
        elif c == "<":
            context["o"] -= 1
        elif c == ">":
            context["o"] += 1
        elif c == 'p' or c == 'r':
            # rest, duration is based on tempo in beats/minute
            if n == 0:
                n = context['l']
            yield 0, 240/n/context['T'], 0
        elif c == 'n':
            yield fq(*divmod(n, 12)), 240/n/context['T'], context['V']
        elif c in step_names:
            # Note
            if n == 0:
                n = context['l']
            octave, step = context['o'], step_names[c]
            yield fq(octave, step), 240/n/context['T'], context['V']
        else:
            # unknown
            raise Exception("What? %r %r %r" % (c, n, dots))

jingle_bells = """
T132V15
b4b4b2b4b4b2b4>d4<g4.a8b1>c4c4c4.c8c4<
b4b4b8b8b4a4a4b4a2>d2<
b4b4b2b4b4b2b4>d4<g4.a8b1>
c4c4c4.c8c4<b4b4b8b8>d4d4c4<a4g2.d4d4b4a4g4d2.d8d8d4b4a4g4e2.e4e4>c4<b4a4f+2.>d4e4d4c4<a4b2.d4d4b4a4g4d2.d8d8d4b4a4g4e2.e4e4>c4<b4a4>d4d4d4d4e4d4c4<a4g2>d2<b4b4b2b4b4b2b4>d4<g4.a8b1>
c4c4c4.c8c4<b4b4b8b8b4a4a4b4a2>d2<b4b4b2b4b4b2b4>d4<g4.a8b1>
c4c4c4.c8c4<b4b4b8b8>d4d4c4<a4g1
"""

joy_to_the_world = """
T118V15
>d4c+8.<b16a4.g8f+4e4d4.a8b4.b8>c+4.c+8d2.&d8d8d8c+8<b8a8a8.g16f+8>d8d8c+8<b8a8a8.g16f+8f+8f+8f+8f+8f+16g16a4.g16f+16e8e8e8e16f+16g4.f+16e16d8>d4<b8a8.g16f+8g8f+4e4d2>d4c+8.<b16a4.g8f+4e4d4.a8b4.b8>c+4.c+8d2.&d8d8d8c+8<b8a8a8.g16f+8>d8d8c+8<b8a8a8.g16f+8f+8f+8f+8f+8f+16g16a4.g16f+16e8e8e8e16f+16g4.f+16e16d8>d4<b8a8.g16f+8g8f+4e4d2>d4c+8.<b16a4.g8f+4e4d4.a8b4.b8>c+4.c+8d2.&d8d8d8c+8<b8a8a8.g16f+8>d8d8c+8<b8a8a8.g16f+8f+8f+8f+8f+8f+16g16a4.g16f+16e8e8e8e16f+16g4.f+16e16d8>d4<b8a8.g16f+8g8f+4e4d2
"""

deck_the_halls = """
T98V15
r2>el32rd16rc+8&c+r<b8&bra8&arb8&br>c+8&c+r<a8&arb16r>c+16rd16rc-16rc+4r<b16ra8&arg+8&g+ra4&a16.r>e4rd16rc+8&c+r<b8&bra8&arb8&br>c+8&c+r<a8&arb16r>c+16rd16rc-16rc+4r<b16ra8&arg+8&g+ra4&a16.rb4r>c+16rd8&dr<b8&br>c+4rd16re8&er<b8&br>c+16rd16re8&erf+16rg+16ra8&arg+8&g+rf+8&f+re4&e16.re4rd16rc+8&c+r<b8&bra8&arb8&br>c+8&c+r<a8&ar>f+16rf+16rf+16rf+16re4rd16rc+8&c+r<b8&bra4&a16.r>e4rd4&d16.rf+16rl16<a.>c+r32er32ar32n73r32ar32er32c+r32dr32er32f+r32dr32er32ar32er32f+r32er32f+r32d<g+.l32r>c+4.e4rd4rf+16rl16b.<a8r>er32a.n73r32a.er32c+.d.e.f+r32d.e8ra.f+.er32f+r32d<g+32>e.c+4.<b4&b32>c+l32rd8&drc-8.c+4rd16.e8&er<b8&br>c+16rd16.e8.f+16.g+16ra8&arg+8&g+rf+8.e4&e16.re4&ea16.c+8&c+re16rl16.a<a>c+e16r32a>c+16r32<aec+f+16r32f+f+f+e4&e32dl8.c+<ba2&a
"""

we_wish_you_a_merry_christmas = """
T150V15
<g>cl8cdc<bl4aaa>dl8dedcl4<bgg>el8efedc4<a4ggl4a>dc-c2<g>cl8cdc<bl4aaa>dl8dedcl4<bgg>el8efedc4<a4ggl4a>dc-c2<g>ccc<b2bb+bag2>dedcg<gg8g8a>dc-c2<g>cl8cdc<bl4aaa>dl8dedcl4<bgg>el8efedc4<a4ggl4a>dc-
"""

RED = (255, 7, 7)
GREEN = (7, 255, 7)
OFF = (0, 0, 0)

colorway = [RED, RED, OFF, GREEN, GREEN]
colors = 10*[0]

cpx.pixels.brightness = 0.2
while True:
    song = random.choice([jingle_bells, joy_to_the_world, deck_the_halls, we_wish_you_a_merry_christmas])
    for f, d, v in fq_iter(song):
        # Play the tone!
        cpx.stop_tone()
        if cpx.switch and v:
            cpx.start_tone(f)
        # Advance the lights!
        for p in range(10):
            cpx.pixels[p] = colorway[colors[p] % len(colorway)]
            colors[p] += random.choice([-1, +1])
        # Finish the tone!
        time.sleep(d)  # ideally, we'd offset the time based on light changes.
