// Fragment shader

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_LIGHT_SHADER

uniform float cx;
uniform float cy;

// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;

void main() { 
  vec4 diffuse_color = vec4 (1.0, 1.0, 1.0, 1.0);
  vec2 c = vec2(cx, cy);
  // Map into -pi, pi range
  vec2 z = vertTexCoord.st * (2 * 3.14) - 3.14;
  //vec2 sinz = vec2(sin(z.x) * ((exp(z.y) + exp(-z.y)) / 2), cos(z.x) * ((exp(z.y) - exp(-z.y)) / 2));
  //z = vec2(c.x * z.x - c.y * z.y, c.x * z.y + c.y * z.x);
  for (int i = 0; i < 20; i++) {
	vec2 sinz = vec2(sin(z.x) * ((exp(z.y) + exp(-z.y)) / 2), cos(z.x) * ((exp(z.y) - exp(-z.y)) / 2));
	z = vec2(c.x * sinz.x - c.y * sinz.y, c.x * sinz.y + c.y * sinz.x);
	if (length(z) > 50) {
	  diffuse_color = vec4 (1.0, 0.0, 0.0, 1.0);
	  break;
	}
  }
  float diffuse = clamp(dot (vertNormal, vertLightDir),0.0,1.0);
  gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);

}