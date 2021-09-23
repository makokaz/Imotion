const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
camera.position.z = 5;

const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.setClearColor("#90e0ef");
document.body.appendChild( renderer.domElement );
const geometry = new THREE.BoxGeometry(0.7,0.7,0.4);
const material = new THREE.MeshLambertMaterial( { color: 0x00df00 } );
var cubes = []
const cube = new THREE.Mesh( geometry, material );
cube.position.x = 6;

var light = new THREE.PointLight(0xFFFF00);
light.position.set(5, 0, 35);
scene.add(light);

function addbots(){
	var l = 12
	var step = 2*Math.PI / l;
	for(var i =0;i<l;i++){
		var acube = new THREE.Mesh( geometry, material );
		acube.position.x = 5
		acube.position.x = r*Math.cos(i*step) ;
		acube.position.y = r*Math.sin(i*step) ;
		
		cubes.push(acube)
		scene.add(acube)
	}
}
var v = 0.1;
var t = 0;
var alpha = Math.PI;
var maxr = 3;
var r = maxr;
addbots();
var incr = 0.01
var sur_r = 2.5;
var hap_r = 2.5;
var sad_r = 2.1;
var anger_r=2;
var anger_sr = 1;
var sinx = 0;
function animate() {
	requestAnimationFrame( animate );
	emotion = document.getElementById('emotion').value;
	if(emotion==="sadness"){
		t+=0.001
		var step = 2*Math.PI / 12;
		var i = 0;
		cubes.forEach(cube=>{
			cube.position.x = sad_r*Math.cos(t + i*step) ;
			cube.position.y = sad_r*Math.sin(t + i*step) ;
			cube.rotation.z = Math.atan2( cube.position.y, cube.position.x ) ;
			i += 1;
		});
    }
	else if(emotion==="anger"){
		// t+=0.005
		var step = 2*Math.PI / 8;
		var i = 0;
		cubes.forEach(cube=>{
			cube.position.x = anger_r*Math.cos(i*step) ;
			cube.position.y = anger_r*Math.sin(i*step) ;
			i += 1;
		});
		cubes[4].position.x += 0.2 ;
		cubes[4].position.y -= 0.3 ;
		cubes[6].position.x += 0.5 ;
		cubes[6].position.y += 0.3 ;
		step = 2*Math.PI / 3;
		for(i=8;i<11;i++){
			cubes[i].position.x = anger_sr*Math.cos(i*step) ;
			cubes[i].position.y = anger_sr*Math.sin(i*step) ;
			step += i/30;
		}
		// console.log(cubes[i])
		cubes[i].position.x = 0.4 ;
		cubes[i].position.y = 0 ;
		t+=0.05
		sinx+=0.5
		var step = 2*Math.PI / 12;
		var i = 0;
		var arr=[];
		var ar = [];
		for(var arr_i=0;arr_i<12; arr_i++){
			for(var arr_j=0;arr_j<2; arr_j++){
				ar.push(Math.random()*0.6);
			}
			arr.push(ar);
		}
		cubes.forEach(cube=>{
			// sinx=sinx%(2*Math.PI);
			// cube.position.x = hap_r*Math.cos(t + i*step) + sinx;
			// cube.position.y = hap_r*Math.sin(t + i*step) + Math.sin(sinx);
			// cube.rotation.z = Math.atan2( cube.position.y, cube.position.x ) ;
			
			cube.position.x += i;
			cube.position.y += 0.5*Math.cos(t)*Math.sin(0.5);
			cube.rotation.z = Math.atan2( cube.position.y, cube.position.x ) ;
			i += 1;
		});
		
    }
    else if(emotion==="surprise"){
		t+=0.005
		var step = 2*Math.PI / 12;
		var i = 0;
		cubes.forEach(cube=>{
			cube.position.x = sur_r*Math.cos(t + i*step) ;
			cube.position.y = sur_r*Math.sin(t + i*step) ;
			cube.rotation.z = Math.atan2( cube.position.y, cube.position.x ) ;
			i += 1;
		});
		
		sur_r += incr;
		if(sur_r>4){
			incr = -incr;
		}
		else if(sur_r<2){
			incr = -incr;
		} 
    }
	else if(emotion==="happiness"){
		// t+=0.5
		sinx+=0.005
		sinx=sinx%(2*Math.PI);
		var step = 2*Math.PI / 12;
		var i = 0;
		cubes.forEach(cube=>{
			cube.position.x = (3+0.5*Math.cos(10*sinx + i*(Math.PI)))*Math.cos(sinx+ i*step);
			cube.position.y = (3+0.5*Math.cos(10*sinx + i*(Math.PI)))*Math.sin(sinx+ i*step);
			cube.rotation.z = Math.atan2( cube.position.y, cube.position.x ) ;
			i += 1;
		});
		
		sur_r += incr;
		if(sur_r>4){
			incr = -incr;
		}
		else if(sur_r<2){
			incr = -incr;
		} 
    }
	
	renderer.render( scene, camera );
}
animate();

