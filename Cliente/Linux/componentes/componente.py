import abc

class Componente(Object):
	
        __metaclass__ = abc.ABCMeta
	
        
        def __init__(self, id):
            self.id = id

	@classmethod
	@abc.abstractmethod
	def set_id(self, id):
		self.id = id


