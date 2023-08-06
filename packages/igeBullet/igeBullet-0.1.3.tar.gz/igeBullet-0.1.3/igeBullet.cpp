#include <Python.h>
#include <stdio.h>
#include "igeBullet_doc_en.h"
#include "igeBullet.h"

#include "btBulletDynamicsCommon.h"
#include "BulletCollision/CollisionDispatch/btGhostObject.h"
#include "BulletDynamics/Character/btKinematicCharacterController.h"

#if defined _WIN32             //WIN32
#   include <time.h>
#   include <Windows.h>
#elif defined __APPLE__
#   include "TargetConditionals.h"
#   if TARGET_OS_IPHONE        //iOS
#       include <sys/types.h>
#   else                       //OSX
#       include <time.h>
#   endif
#	include <mach/mach_time.h>
#elif defined __ANDROID__      //Android
#   include <sys/time.h>
#   include <time.h>
#endif

float* pyObjToFloat(PyObject* obj, float* f, int& d) {
	if (f) {
		f[0] = f[1] = f[2] = f[3] = 0.0f;
	}
	if (PyTuple_Check(obj)) {
		d = (int)PyTuple_Size(obj);
		if (d > 4) d = 4;
		for (int j = 0; j < d; j++) {
			PyObject* val = PyTuple_GET_ITEM(obj, j);
			f[j] = (float)PyFloat_AsDouble(val);
		}
	}
	else if (PyList_Check(obj)) {
		d = (int)PyList_Size(obj);
		if (d > 4) d = 4;
		for (int j = 0; j < d; j++) {
			PyObject* val = PyList_GET_ITEM(obj, j);
			f[j] = (float)PyFloat_AsDouble(val);
		}
	}
	else {
		PyErr_SetString(PyExc_ValueError, "invalid arguments");
		return  NULL;
	}
	return f;
}

//////////////////////////////////////////////////////////////////////
//Shape
//////////////////////////////////////////////////////////////////////
#if true

PyObject* shape_new(PyTypeObject* type, PyObject* args, PyObject* kw) {

	static char* kwlist[] = { "type","radius","height","halfExtents","upAxis","normal","constant", NULL };
	int shapetype;
	PyObject* radius=nullptr;
	PyObject* height = nullptr;
	PyObject* halfExtents = nullptr;
	PyObject* upAxis = nullptr;
	PyObject* normal = nullptr;
	PyObject* constant = nullptr;

	if (!PyArg_ParseTupleAndKeywords(args, kw, "i|OOOOOO", kwlist,
		&shapetype, &radius, &height, &halfExtents, &upAxis, &normal, &constant))
		return NULL;

	float f[4];
	int d;
	float* fp;
	btCollisionShape* shape=nullptr;

	switch (shapetype) {
	case BOX_SHAPE_PROXYTYPE:
		fp = pyObjToFloat(halfExtents, f, d);
		shape = new btBoxShape(btVector3(f[0], f[1], f[2]));
		break;
	case SPHERE_SHAPE_PROXYTYPE:
		break;
	case CAPSULE_SHAPE_PROXYTYPE:
		break;
	case CONE_SHAPE_PROXYTYPE:
		break;
	case CYLINDER_SHAPE_PROXYTYPE:
		break;
	case COMPOUND_SHAPE_PROXYTYPE:
		break;
	}

	shape_obj* self = (shape_obj*)type->tp_alloc(type, 0);
	self->btshape = shape;

	return (PyObject*)self;
}

void  shape_dealloc(shape_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* shape_str(shape_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "physics shape object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

PyMethodDef shape_methods[] = {
	{ NULL,	NULL }
};

PyGetSetDef shape_getsets[] = {
	{ NULL, NULL }
};

PyTypeObject ShapeType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeBullet.shape",					/* tp_name */
	sizeof(shape_obj),                  /* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)shape_dealloc,			/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)shape_str,                /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	shape_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	shape_methods,						/* tp_methods */
	0,                                  /* tp_members */
	shape_getsets,                      /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	shape_new,							/* tp_new */
	0,									/* tp_free */
};
#endif
//////////////////////////////////////////////////////////////////////
//Rigidbody
//////////////////////////////////////////////////////////////////////
#if true
PyObject* rigidbody_new(PyTypeObject* type, PyObject* args, PyObject* kw) {

	static char* kwlist[] = { "shape","mass","pos","rot","activate", NULL };

	shape_obj* shape_o = nullptr;
	PyObject* mass_o = nullptr;
	PyObject* pos_o = nullptr;
	PyObject* rot_o = nullptr;
	int activate = 1;

	if (!PyArg_ParseTupleAndKeywords(args, kw, "OOOO|i", kwlist,
		&shape_o, &mass_o, &pos_o, &rot_o, &activate))
		return NULL;

	float f[4];
	int d;
	float* fp;

	btCollisionShape* shape = nullptr;

	btTransform transform;
	transform.setIdentity();

	fp = pyObjToFloat(pos_o, f, d);
	transform.setOrigin(btVector3(fp[0], fp[1], fp[2]));
	fp = pyObjToFloat(rot_o, f, d);
	transform.setRotation(btQuaternion(fp[0], fp[1], fp[2],fp[3]));
	float mass = (float)PyFloat_AsDouble(mass_o);
	bool isDynamic = (mass != 0.f);

	btVector3 localInertia(0, 0, 0);
	if (isDynamic) ((btCollisionShape*)(shape_o->btshape))->calculateLocalInertia(mass, localInertia);

	btDefaultMotionState* myMotionState = new btDefaultMotionState(transform);
	btRigidBody::btRigidBodyConstructionInfo rbInfo(mass, myMotionState, ((btCollisionShape*)(shape_o->btshape)), localInertia);

	btRigidBody* body = new btRigidBody(rbInfo);
	if(!activate)
		body->forceActivationState(WANTS_DEACTIVATION);

	body->setContactProcessingThreshold(BT_LARGE_FLOAT);
	if (!isDynamic) body->setCollisionFlags(body->getCollisionFlags() | btCollisionObject::CF_STATIC_OBJECT);

	rigidbody_obj* self = (rigidbody_obj*)type->tp_alloc(type, 0);
	self->btbody = body;

	return (PyObject*)self;
}

void  rigidbody_dealloc(rigidbody_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* rigidbody_str(rigidbody_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "physics rigidbody object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

PyMethodDef rigidbody_methods[] = {
	{ NULL,	NULL }
};

PyObject* rigidbody_getposition(rigidbody_obj* self)
{
	btVector3& pos = ((btRigidBody*)self->btbody)->getWorldTransform().getOrigin();
	PyObject* out = PyTuple_New(3);
	if (!out) return NULL;
	PyTuple_SetItem(out, 0, PyFloat_FromDouble(pos.getX()));
	PyTuple_SetItem(out, 1, PyFloat_FromDouble(pos.getY()));
	PyTuple_SetItem(out, 2, PyFloat_FromDouble(pos.getZ()));
	return out;
}
int rigidbody_setposition(rigidbody_obj* self, PyObject* value)
{
	int d1;
	float buff[4];
	float* v1 = pyObjToFloat((PyObject*)value, buff, d1);
	if (!v1) return NULL;

	btVector3 btpos(buff[0], buff[1], buff[2]);
	btTransform& trans = ((btRigidBody*)self->btbody)->getWorldTransform();
	trans.setOrigin(btpos);
	//if (world) world->GetWorld()->updateSingleAabb(object);
	return 0;
}

PyObject* rigidbody_getrotation(rigidbody_obj* self)
{
	btQuaternion rot = ((btRigidBody*)self->btbody)->getWorldTransform().getRotation();
	PyObject* out = PyTuple_New(3);
	if (!out) return NULL;
	PyTuple_SetItem(out, 0, PyFloat_FromDouble(rot.getX()));
	PyTuple_SetItem(out, 1, PyFloat_FromDouble(rot.getY()));
	PyTuple_SetItem(out, 2, PyFloat_FromDouble(rot.getZ()));
	PyTuple_SetItem(out, 3, PyFloat_FromDouble(rot.getW()));
	return out;
}
int rigidbody_setrotation(rigidbody_obj* self, PyObject* value)
{
	int d1;
	float buff[4];
	float* v1 = pyObjToFloat((PyObject*)value, buff, d1);
	if (!v1) return NULL;

	btQuaternion btRot(buff[0], buff[1], buff[2], buff[3]);
	btTransform& trans = ((btRigidBody*)self->btbody)->getWorldTransform();
	trans.setRotation(btRot);
	//if (world) world->GetWorld()->updateSingleAabb(object);
	return 0;
}




PyGetSetDef rigidbody_getsets[] = {
	{ const_cast<char*>("position"), (getter)rigidbody_getposition, (setter)rigidbody_setposition,rigidbody_position_doc, NULL },
	{ const_cast<char*>("rotation"), (getter)rigidbody_getrotation, (setter)rigidbody_setrotation,rigidbody_rotation_doc, NULL },


	{ NULL, NULL }
};

PyTypeObject RigidBodyType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeBullet.rigidBody",				/* tp_name */
	sizeof(rigidbody_obj),              /* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)rigidbody_dealloc,		/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)rigidbody_str,            /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	rigidbody_doc,						/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	rigidbody_methods,					/* tp_methods */
	0,                                  /* tp_members */
	rigidbody_getsets,                  /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	rigidbody_new,						/* tp_new */
	0,									/* tp_free */
};


#endif
//////////////////////////////////////////////////////////////////////
//World
//////////////////////////////////////////////////////////////////////
#if true
PyObject* dynworld_new(PyTypeObject* type, PyObject* args, PyObject* kw) {

	btBroadphaseInterface* broadphase = nullptr;
	btCollisionDispatcher* dispatcher = nullptr;
	btGhostPairCallback* ghostPairCallback = nullptr;
	btConstraintSolver* solver = nullptr;
	btDefaultCollisionConfiguration* collisionConfiguration = nullptr;

	///collision configuration contains default setup for memory, collision setup
	btDefaultCollisionConstructionInfo ci;
	ci.m_defaultStackAllocatorSize = 256 * 1024;
	ci.m_defaultMaxPersistentManifoldPoolSize = 512;
	ci.m_defaultMaxCollisionAlgorithmPoolSize = 512;
	collisionConfiguration = new btDefaultCollisionConfiguration(ci);
	//collisionConfiguration->setConvexConvexMultipointIterations();

	///use the default collision dispatcher. For parallel processing you can use a diffent dispatcher (see Extras/BulletMultiThreaded)
	dispatcher = new btCollisionDispatcher(collisionConfiguration);

	//broadphase = _new btAxisSweep3(btVector3(-100,-10,-100),btVector3(100,10,100));
	broadphase = new btDbvtBroadphase();
	ghostPairCallback = new btGhostPairCallback();
	broadphase->getOverlappingPairCache()->setInternalGhostPairCallback(ghostPairCallback);

	solver = new btSequentialImpulseConstraintSolver;

	btDiscreteDynamicsWorld* world = new btDiscreteDynamicsWorld(dispatcher,broadphase,solver,collisionConfiguration);

	world_obj* self = (world_obj*)type->tp_alloc(type, 0);
	self->broadphase = broadphase;
	self->dispatcher = dispatcher;
	self->solver = solver;
	self->ghostPairCallback = ghostPairCallback;
	self->collisionConfiguration = collisionConfiguration;
	self->btworld = world;

#if defined _WIN32
	QueryPerformanceFrequency((LARGE_INTEGER*) & (self->freq));
#elif defined __ANDROID__
#else
	mach_timebase_info(&base);
#endif
	return (PyObject*)self;
}

void  dynworld_dealloc(world_obj* self)
{
	Py_TYPE(self)->tp_free(self);
}

PyObject* dynworld_str(world_obj* self)
{
	char buf[64];
	snprintf(buf, 64, "physics world object");
	return _PyUnicode_FromASCII(buf, strlen(buf));
}

static PyObject* dynworld_add(world_obj* self, PyObject* args) {
	PyObject* obj;
	if (!PyArg_ParseTuple(args, "O", &obj))return NULL;
	if (obj->ob_type == &RigidBodyType) {
		((btDiscreteDynamicsWorld*)self->btworld)->addRigidBody((btRigidBody*)(((rigidbody_obj*)obj)->btbody));
	}
	else {
		PyErr_SetString(PyExc_TypeError, "parameter error.");
		return NULL;
	}
	Py_INCREF(Py_None);
	return Py_None;
}
static PyObject* dynworld_remove(world_obj* self, PyObject* args) {
	PyObject* obj;
	if (!PyArg_ParseTuple(args, "O", &obj))return NULL;
	if (obj->ob_type == &RigidBodyType) {
		((btDiscreteDynamicsWorld*)self->btworld)->removeRigidBody((btRigidBody*)(((rigidbody_obj*)obj)->btbody));
	}
	else {
		PyErr_SetString(PyExc_TypeError, "parameter error.");
		return NULL;
	}
	Py_INCREF(Py_None);
	return Py_None;
}

static PyObject* dynworld_step(world_obj* self, PyObject* args) {

	double cpuTime;
#if defined _WIN32
	static LARGE_INTEGER	cuurentTime;
	QueryPerformanceCounter(&cuurentTime);
	LARGE_INTEGER* freq = (LARGE_INTEGER*) & (self->freq);
	cpuTime = (double)cuurentTime.QuadPart / (double)freq->QuadPart;
#elif defined __ANDROID__
	struct timespec tv;
	clock_gettime(CLOCK_MONOTONIC, &tv);
	cpuTime = (double)tv.tv_sec + (double)tv.tv_nsec / 1000000000.0;
#else
	uint64_t t = mach_absolute_time();
	cpuTime = (double)t * (double)base.numer / (double)base.denom / 1000000000.0;
#endif
	double elapsedTime = cpuTime - self->lasttime;
	self->lasttime = cpuTime;
	if (elapsedTime > 0.333333333333)elapsedTime = 0.333333333333;
	((btDiscreteDynamicsWorld*)self->btworld)->stepSimulation((btScalar)elapsedTime);

	Py_INCREF(Py_None);
	return Py_None;
}
static PyObject* dynworld_wait(world_obj* self, PyObject* args) {
	Py_INCREF(Py_None);
	return Py_None;
}

PyObject* dynworld_getgravity(world_obj* self)
{
	btVector3 vec = ((btDiscreteDynamicsWorld*)self->btworld)->getGravity();
	PyObject* out = PyTuple_New(3);
	if (!out) return NULL;
	PyTuple_SetItem(out, 0, PyFloat_FromDouble(vec.getX()));
	PyTuple_SetItem(out, 1, PyFloat_FromDouble(vec.getY()));
	PyTuple_SetItem(out, 2, PyFloat_FromDouble(vec.getZ()));
	return out;
}
int dynworld_setgravity(world_obj* self, PyObject* value)
{
	int d1;
	float buff[4];
	float* v1 = pyObjToFloat((PyObject*)value, buff, d1);
	if (!v1) return NULL;
	((btDiscreteDynamicsWorld*)self->btworld)->setGravity(btVector3(buff[0], buff[1], buff[2]));
	return 0;
}



PyMethodDef dynworld_methods[] = {
	{ "add", (PyCFunction)dynworld_add, METH_VARARGS, add_doc},
	{ "remove", (PyCFunction)dynworld_remove, METH_VARARGS, remove_doc},
	{ "step", (PyCFunction)dynworld_step, METH_VARARGS, step_doc},
	{ "wait", (PyCFunction)dynworld_wait, METH_VARARGS, wait_doc},
	{ NULL,	NULL }
};

PyGetSetDef dynworld_getsets[] = {
	{ const_cast<char*>("gravity"), (getter)dynworld_getgravity, (setter)dynworld_setgravity,gravity_doc, NULL },
	{ NULL, NULL }
};

PyTypeObject DynamicsWorldType = {
	PyVarObject_HEAD_INIT(NULL, 0)
	"igeBullet.dynamicsWorld",					/* tp_name */
	sizeof(world_obj),					/* tp_basicsize */
	0,                                  /* tp_itemsize */
	(destructor)dynworld_dealloc,			/* tp_dealloc */
	0,                                  /* tp_print */
	0,							        /* tp_getattr */
	0,                                  /* tp_setattr */
	0,                                  /* tp_reserved */
	0,                                  /* tp_repr */
	0,					                /* tp_as_number */
	0,                                  /* tp_as_sequence */
	0,                                  /* tp_as_mapping */
	0,                                  /* tp_hash */
	0,                                  /* tp_call */
	(reprfunc)dynworld_str,			   /* tp_str */
	0,                                  /* tp_getattro */
	0,                                  /* tp_setattro */
	0,                                  /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT,					/* tp_flags */
	dynworld_doc,							/* tp_doc */
	0,									/* tp_traverse */
	0,                                  /* tp_clear */
	0,                                  /* tp_richcompare */
	0,                                  /* tp_weaklistoffset */
	0,									/* tp_iter */
	0,									/* tp_iternext */
	dynworld_methods,						/* tp_methods */
	0,                                  /* tp_members */
	dynworld_getsets,				      /* tp_getset */
	0,                                  /* tp_base */
	0,                                  /* tp_dict */
	0,                                  /* tp_descr_get */
	0,                                  /* tp_descr_set */
	0,                                  /* tp_dictoffset */
	0,                                  /* tp_init */
	0,                                  /* tp_alloc */
	dynworld_new,							/* tp_new */
	0,									/* tp_free */
};

#endif

//////////////////////////////////////////////////////////////////////
//pyxBullet
//////////////////////////////////////////////////////////////////////
static PyMethodDef pyxBullet_methods[] = {
{ nullptr, nullptr, 0, nullptr }
};

static PyModuleDef igeBullet_module = {
	PyModuleDef_HEAD_INIT,
	"igeBullet",								// Module name to use with Python import statements
	"Bullet wrapper for pyxie game engine.",	// Module description
	0,
	pyxBullet_methods							// Structure that defines the methods of the module
};

PyMODINIT_FUNC PyInit_igeBullet() {
	PyObject* module = PyModule_Create(&igeBullet_module);

	if (PyType_Ready(&ShapeType) < 0) return NULL;
	if (PyType_Ready(&RigidBodyType) < 0) return NULL;
	if (PyType_Ready(&DynamicsWorldType) < 0) return NULL;

	Py_INCREF(&ShapeType);
	PyModule_AddObject(module, "shape", (PyObject*)& ShapeType);
	Py_INCREF(&RigidBodyType);
	PyModule_AddObject(module, "rigidBody", (PyObject*)& RigidBodyType);
	Py_INCREF(&DynamicsWorldType);
	PyModule_AddObject(module, "dynamicsWorld", (PyObject*)& DynamicsWorldType);

	return module;
}
