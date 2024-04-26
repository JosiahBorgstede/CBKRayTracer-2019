def color(r, world, lights, depth=0, curAlbedo=np.array([1.0, 1.0, 1.0])):
    hit = world.hit(r, 0.001, float('inf')) # Check if we hit anything
    if hit: # If we did
        scattered, albedo = hit['material'].scatter(r, hit) # Get the new ray and the color
        if scattered:
            newAlbedo = np.multiply(curAlbedo, albedo) # Set up the running color
            lightSum = np.array([0.0, 0.0, 0.0])
            nonLights = [x for x in world.hitables if x not in lights]
            tempWorld = hitable.HitableList(nonLights) # This is inefficient - considering making a SAH_BVH and passing that into the function instead of making one of these every time
            if isinstance(hit['material'], material.Diffuse):
                for light in lights:
                    L_m = light.getPointOn() - hit['p']
                    distanceToL = np.linalg.norm(L_m)
                    dirToL = L_m/distanceToL
                    shadowRay = ray.Ray(hit['p'], dirToL)

                    hitShadow = tempWorld.hit(shadowRay, 0.001, distanceToL)
                    if hitShadow and hitShadow['t']+0.001 < distanceToL:
                        continue
                    normalDotL = np.dot(dirToL, hit['normal'])
                    if normalDotL > 0:
                        lightSum += normalDotL*np.multiply(newAlbedo, light.material.emitted(hit))
                        # rayReflectDir = -material.reflect(dirToL, hit['normal'])
                        # rayReflectDotOriginal = np.dot(rayReflectDir, -r.direction)
                        # if rayReflectDotOriginal > 0:
                        #     lightSum += pow(rayReflectDotOriginal, 32)*np.multiply(newAlbedo, light.material.emitted(hit))
            lightSum = np.minimum(lightSum, 1.0)

            if depth < 2:
                if isinstance(hit['material'], material.Diffuse):
                    # uncomment this for indirect lighting
                    #if random.uniform(0, 1) <np.mean(lightSum):
                        #return lightSum # Find the color from the reflected ray
                    #else:
                       return color(scattered, world, lights, depth+1, newAlbedo)
                else:
                    return color(scattered, world, lights, depth+1, newAlbedo)
            else:
                return lightSum
        else:
            return np.multiply(curAlbedo, hit['material'].emitted(hit)) # This is for our lights
    else: # Use a background color
        return np.multiply(curAlbedo, np.array([1.0, 1.0, 1.0]))
