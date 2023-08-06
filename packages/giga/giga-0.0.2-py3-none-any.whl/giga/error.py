import giga

log = giga.logs.get_logger(__name__)

class NotImplementedFor(ValueError):

  def __init__(self, platform):
    super().__init__(f'Config not implemented for {platform}')
