// Fragment shader
// The fragment shader is run once for every pixel
// It can change the color and transparency of the fragment.

#ifdef GL_ES
precision mediump float;
precision mediump int;
#endif

#define PROCESSING_TEXLIGHT_SHADER

// Set in Processing
uniform sampler2D my_texture;
uniform sampler2D my_mask;
uniform float blur_flag;

// These values come from the vertex shader
varying vec4 vertColor;
varying vec3 vertNormal;
varying vec3 vertLightDir;
varying vec4 vertTexCoord;

void main() { 

  // grab the color values from the texture and the mask
  vec4 diffuse_color = texture2D(my_texture, vertTexCoord.xy);
  vec4 mask_color = texture2D(my_mask, vertTexCoord.xy);

  // half sheep, half mask
  //if (vertTexCoord.x > 0.5)
  //  diffuse_color = mask_color;

  // simple diffuse shading model
  float diffuse = clamp(dot (vertNormal, vertLightDir),0.0,1.0);

  //gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);
  
  float mask_value = mask_color.r;
  if (mask_value <= 0.5 && blur_flag == 1) {
	  vec4 blurColor = vec4(0.0);
	  float blur = .002;
	  if (mask_value < 0.1) {
		blur = .01;
	  }
	  
	  blurColor += texture2D(my_texture, vec2(vertTexCoord.x - blur, vertTexCoord.y - blur));
	  blurColor += texture2D(my_texture, vec2(vertTexCoord.x, vertTexCoord.y - blur));
	  blurColor += texture2D(my_texture, vec2(vertTexCoord.x + blur, vertTexCoord.y - blur));
	  blurColor += texture2D(my_texture, vec2(vertTexCoord.x - blur, vertTexCoord.y));
	  blurColor += texture2D(my_texture, vec2(vertTexCoord.x, vertTexCoord.y));
	  blurColor += texture2D(my_texture, vec2(vertTexCoord.x + blur, vertTexCoord.y));
	  blurColor += texture2D(my_texture, vec2(vertTexCoord.x - blur, vertTexCoord.y + blur));
	  blurColor += texture2D(my_texture, vec2(vertTexCoord.x, vertTexCoord.y + blur));
	  blurColor += texture2D(my_texture, vec2(vertTexCoord.x + blur, vertTexCoord.y + blur));
	  diffuse_color = blurColor * vec4(1.0/9, 1.0/9, 1.0/9, 1.0);
  }
  gl_FragColor = vec4(diffuse * diffuse_color.rgb, 1.0);
  
}
