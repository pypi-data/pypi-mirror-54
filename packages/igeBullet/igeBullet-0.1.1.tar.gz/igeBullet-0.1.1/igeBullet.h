#include <Python.h>

typedef struct {
	PyObject_HEAD
		void* btshape;
} shape_obj;

typedef struct {
	PyObject_HEAD
		void* btbody;
		PyObject* world;
} rigidbody_obj;

typedef struct {
	PyObject_HEAD
		void* broadphase;
		void* dispatcher;
		void* solver;
		void* ghostPairCallback;
		void* collisionConfiguration;
		void* btworld;
		__int64 freq;
		double lasttime;
} world_obj;
