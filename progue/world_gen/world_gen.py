import sys
import math
import random
from noise import snoise2
from chunk import Chunk
from progue.utils.file_management import load_chunk, save_chunk
from progue.debug.logger import log_call, log_endl, log_message

DEFAULT_LACUNARITY = 2.0
DEFAULT_GAIN = 0.65
DEFAULT_OCTAVES = 7
DEBUG_MODE = False


class WorldBuilder(object):
    """ Handle building the world """

    def __init__(self, world_width, world_height, chunk_width, chunk_height):
        self.world_width = world_width
        self.world_height = world_height

        self.chunk_width = chunk_width
        self.chunk_height = chunk_height

        self.num_chunks_x = self.world_width / self.chunk_width
        self.num_chunks_y = self.world_height / self.chunk_height

    def __build_blank_map(self):
        blank_map = []
        for j in xrange(self.num_chunks_y):
            blank_map.append([])
            for i in xrange(self.num_chunks_x):
                blank_map[j].append(
                    Chunk(x=i, y=j, width=self.chunk_width, height=self.chunk_height, debug=DEBUG_MODE))

        return blank_map

    def make_map(self):
        res = []
        base = random.randint(-self.world_width, self.world_width)

        for j in xrange(self.world_height):
            res.append([])
            for i in xrange(self.world_width):
                res[j].append(self.__fractal(
                    x=i, y=j, hgrid=self.world_width, base=base))
        return res

    def chunkify_map(self, to_chunkify):
        tiles = self.__build_blank_map()
        for j in xrange(len(to_chunkify)):
            for i in xrange(len(to_chunkify[j])):
                (chunk_x, chunk_y) = (int(math.floor(i / self.chunk_width)), int(math.floor(j / self.chunk_height)))
                (x, y) = (i % self.chunk_width, j % self.chunk_height)
                tiles[chunk_y][chunk_x].raw_map[y][x] = to_chunkify[j][i]
        return tiles

    def generate_world(self):
        to_chunkify = self.make_map()
        tiles = self.chunkify_map(to_chunkify)
        log_message('Created {x} chunks.'.format(
            x=self.num_chunks_x * self.num_chunks_y))
        log_message('Chunk size: {x}'.format(x=self.chunk_width))

        return tiles

    def __fractal(self, x, y, hgrid, base, num_octaves=DEFAULT_OCTAVES, lacunarity=DEFAULT_LACUNARITY, gain=DEFAULT_GAIN):
        """ A more refined approach but has a much slower run time """
        noise = []
        frequency = 1.0 / hgrid
        amplitude = gain

        for i in xrange(num_octaves):
            noise.append(
                snoise2(
                    x=x * frequency,
                    y=y * frequency,
                    base=base
                ) * amplitude
            )

            frequency *= lacunarity
            amplitude *= gain

        return sum(noise)
