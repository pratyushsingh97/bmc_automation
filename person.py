class Person(object):
	person_list = [] 
	
	def __init__(self, ibm_id=None, service_name=None, service_inst=None, region=None, 
				 resource_type=None, resource=None, platform_viewer=None, platform_editor=None, 
				 platform_admin=None, service_reader=None, service_writer=None, service_manager=None,
				 rg_id=None, rg_viewer=None, rg_operator=None, rg_editor=None, rg_admin=None):
		
		self._ibm_id = ibm_id
		self._service_name = service_name
		self._service_inst = service_inst
		self._region = region
		self._resource_type = resource_type
		self._resource = resource
		self._platform_viewer = platform_viewer
		self._platform_editor = platform_editor
		self._platform_administrator = platform_admin
		self._service_reader = service_reader
		self._service_writer = service_writer
		self._service_manager = service_manager
		self._ag = None
		
		# rg
		self._rg_id = rg_id
		self._rg_viewer = rg_viewer
		self._rg_operator = rg_operator
		self._rg_editor = rg_editor
		self._rg_admin = rg_admin
   
	@property
	def rg_id(self):
		return self._rg_id
	
	@rg_id.setter
	def rg_id(self, id_):
		self._rg_id = id
		
	@property
	def rg_viewer(self):
		return self._rg_viewer
	
	@rg_viewer.setter
	def rg_viewer(self, viewer):
		self._rg_viewer = viewer
	
	@property
	def rg_operator(self):
		return self._rg_operator
	
	@rg_operator.setter
	def rg_operator(self, operator):
		self._rg_operator = operator
	
	@property
	def rg_editor(self):
		return self._rg_editor
	
	@rg_editor.setter
	def rg_editor(self, editor):
		self._rg_editor = editor
	
	
	@property
	def rg_admin(self):
		return self._rg_admin
	
	@rg_admin.setter
	def rg_admin(self, admin):
		self._rg_admin = admin
	
	@property
	def ibm_id(self):
		return self._ibm_id
	
	@ibm_id.setter
	def ibm_id(self, _id):
		self._ibm_id = _id
	
	@property
	def service_name(self):
		return self._service_name
	
	@service_name.setter
	def service_name(self, name):
		self._service_name = name
	
	@property
	def service_inst(self):
		return self._service_inst
	
	@service_inst.setter
	def service_inst(self, inst):
		self._service_inst = inst
	
	@property
	def region(self):
		return self._region
	
	@region.setter
	def region(self, reg):
		self._region = reg

	@property
	def resource_type(self):
		return self._resource_type
	
	@resource_type.setter
	def resource_type(self, rt):
		self._resource_type = rt

	@property
	def resource(self):
		return self._resource

	@resource.setter
	def resource(self, id):
		self._resource = id

	@property
	def platform_viewer(self):
		return self._platform_viewer
	
	@platform_viewer.setter
	def platform_viewer(self, viewer):
		self._platform_viewer = viewer
	
	@property
	def platform_editor(self):
		return self._platform_editor

	@platform_editor.setter
	def platform_editor(self, editor):
		self._platform_editor = editor
	
	@property
	def platform_administrator(self):
		return self._platform_administrator
	
	@platform_administrator.setter
	def platform_admin(self, admin):
		self._platform_administrator = admin
	
	@property
	def service_reader(self):
		return self._service_reader

	@service_reader.setter
	def service_reader(self, reader):
		self._service_reader = reader
	
	@property
	def service_writer(self):
		return self._service_writer
	
	@service_writer.setter
	def service_writer(self, writer):
		self._service_writer = writer
	
	@property
	def service_manager(self):
		return self._service_manager
	
	@service_manager.setter
	def service_manager(self, manager):
		self._service_manager = manager
	
	
	@property
	def ag(self):
		return self._ag
	
	@ag.setter
	def ag(self, group):
		self._ag = group
	

	




	