// Fragment shader

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_LIGHT_SHADER

// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;

void main() { 
  float diffuse = clamp(dot (vertNormal, vertLightDir),0.0,1.0);
  vec4 diffuse_color = vec4(0.0, 1.0, 1.0, 1.0);
  gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);
  // Rotate coordinates
  mat2 rot = mat2(cos(radians(45)), -sin(radians(45)),
                  sin(radians(45)), cos(radians(45)));
  vec2 coord = vertTexCoord.st;
  coord += vec2(-.5, -.5);
  coord = rot * coord;
  coord += vec2(.5, .5);
  // Set up cutout boundaries
  float off = .20;
  float sl = .50 - (.15 / 2);
  float sr = .50 + (.15 / 2);
  float tb = .50 + (.15 / 2);
  float tt = .50 - (.15 / 2);
  // Move ts to the top
  tb -= off + off;
  tt -= off + off;
  // top square
  if (coord.s > sl && coord.s < sr && coord.t > tt && coord.t < tb) {
	gl_FragColor = vec4(0.2, 0.4, 1.0, 0.0);
  }
  // second set of squares
  tb += off;
  tt += off;
  sl -= off;
  sr -= off;
  for (int i = 0; i < 3; i++) {
	if (coord.s > sl && coord.s < sr && coord.t > tt && coord.t < tb) {
		gl_FragColor = vec4(0.2, 0.4, 1.0, 0.0);
	}
	sl += off;
	sr += off;
  }
  // third set of squares
  tb += off;
  tt += off;
  sl -= off + off + off + off;
  sr -= off + off + off + off;
  for (int i = 0; i < 5; i++) {
	if (coord.s > sl && coord.s < sr && coord.t > tt && coord.t < tb) {
		gl_FragColor = vec4(0.2, 0.4, 1.0, 0.0);
	}
	sl += off;
	sr += off;
  }
  // fourth set of squares
  tb += off;
  tt += off;
  sl -= off + off + off + off;
  sr -= off + off + off + off;
  for (int i = 0; i < 3; i++) {
	if (coord.s > sl && coord.s < sr && coord.t > tt && coord.t < tb) {
		gl_FragColor = vec4(0.2, 0.4, 1.0, 0.0);
	}
	sl += off;
	sr += off;
  }
  // last square
  tb += off;
  tt += off;
  sl -= off + off;
  sr -= off + off;
  if (coord.s > sl && coord.s < sr && coord.t > tt && coord.t < tb) {
	gl_FragColor = vec4(0.2, 0.4, 1.0, 0.0);
  }
}

