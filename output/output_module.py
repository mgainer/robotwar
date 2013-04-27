import imp
import os

def load_outputter(name, play_history, world_map):
  fp, path, desc = imp.find_module(os.path.join('output', name.lower()))
  output_module = imp.load_module(name, fp, path, desc)
  outputter = eval('output_module.%s(play_history, world_map)' % name)
  return outputter


class Output:
  def __init__(self, play_history, world_map):
    self._play_history = play_history
    self._world_map = world_map

  def get_output(self, writable):
    writable.write('Ooops!  Output module %s ' % str(self.__class__) +
                   'should have implemented output() function.\n')
