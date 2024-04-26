for(unsigned int i = 0; i < lights.size(); ++i) { for light in lights
	Vector directionToL(lights[i].location - collisionPoint); L_m
	if(lightRadius) {
	  directionToL = directionToL + (lightRadius*RandomHelper::randomInHemisphereOf(directionToL));
#	}
#	if (lights[i].atInfinity == true) {
#	  directionToL = lights[i].location;
#	}
#	double distToL = Vector::norm(directionToL);
	directionToL.normalize();
#	Ray lightRay(collisionPoint, directionToL);
	CastResult lightResult = castRay(lightRay);
	t = lightResult.t;
#	if(t < distToL && lightResult.hitObject->material->castShadow) {
#	  continue;
#	}
	double normalDotDirL = Vector::dot(directionToL, normal);
	if(normalDotDirL > 0) {
	  returnVal = returnVal + normalDotDirL*pairwiseMultiply(lights[i].colorEmittance, hitObject->getDiffuse(collisionPoint));
	  Vector rayReflectDir(2*normalDotDirL*normal - directionToL);
	  rayReflectDir.normalize();
	  double otherThing = Vector::dot(rayReflectDir, -1.0*ray.direction);
	  if(otherThing > 0) {
		returnVal = returnVal + pow(otherThing, hitObject->getSpecularCoefficient(collisionPoint))*(pairwiseMultiply(hitObject->getSpecular(collisionPoint), lights[i].colorEmittance));
	  }
	}
}
if(depth > 0) {
	Vector attenuate(hitObject->getAttenuation(collisionPoint));
	Vector reflected(0.0, 0.0, 0.0);
	if(!(attenuate(0) == 0 && attenuate(1) == 0 && attenuate(2) == 0)) {
	  Vector rayBounceDir(2*Vector::dot(normal, -1*ray.direction)*normal + ray.direction);
	  rayBounceDir.normalize();
	  Vector randomDir(3);
	  randomDir = rayBounceDir;
	  Ray rayBounce(collisionPoint, randomDir);
	  reflected = pairwiseMultiply(hitObject->getAttenuation(collisionPoint), traceRay(rayBounce, depth-1));
	}
	if(hitObject->getTransparency(collisionPoint)) {
	  Ray refract = hitObject->getRefractRay(-1*ray.direction, collisionPoint);
	  if(!(refract.direction(0) == 0 && refract.direction(1) == 0 && refract.direction(2) == 0)) {
		Vector refracted = traceRay(refract, depth-1);
		if(!hitObject->material->semiTransparent) {
		  returnVal = returnVal + reflected + hitObject->getTransparency(collisionPoint)*pairwiseMultiply(hitObject->getRefractivityAmount(collisionPoint, 1), refracted);
		}
		else {
		  returnVal = (1-hitObject->getTransparency(collisionPoint))*(returnVal + reflected) + hitObject->getTransparency(collisionPoint)*pairwiseMultiply(hitObject->getRefractivityAmount(collisionPoint, 1), refracted);
		}
	  }
	  else {
		returnVal = returnVal + reflected;
	  }
	}
	else {
	  returnVal = returnVal + reflected;
	}
}
return returnVal;
