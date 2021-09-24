const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );
camera.position.z = 5;

const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.setClearColor("#90e0ef");
document.body.appendChild( renderer.domElement );
var geometry = new THREE.BoxGeometry(0.7,0.7,0.4);
var material = new THREE.MeshLambertMaterial( { color: 0xb90e0a } );
var cubes = []
const cube_ = new THREE.Mesh( geometry, material );
var cube = new THREE.Group()
var model_loader = new THREE.GLTFLoader();
model_loader.load(
    './static/drone.glb',
    function ( gltf ) {
    
		console.log(gltf)
        cube = gltf.scene.getObjectByName("Syma_X8C001")
        cube.scale.set(0.07,0.07,0.07)
        THREE.BufferGeometry.prototype.copy.call(geometry, cube.geometry);
    }, undefined, function ( error ) {
        console.error( error );
        console.log("wow")
    } 
);

const num_bots = 12;
var light = new THREE.PointLight(0xFFFF00);
light.position.set(5, 0, 35);
scene.add(light);

function addbots(){
	var l = num_bots
	var step = 2*Math.PI / l;
    //var acube = new THREE.Group()
	for(var i =0;i<l;i++){
		var acube = new THREE.Mesh( geometry, material );
        acube.scale.set(0.07,0.07,0.07)
        acube.rotation.x +=1;
		//acube = cube.clone()
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
var arr=[];
var ar = [];
for(var arr_i=0;arr_i<num_bots; arr_i++){
	for(var arr_j=0;arr_j<2; arr_j++){
		ar.push(Math.random()*0.3 + 0.01);
	}
	arr.push(ar);
}

function animate() {
	requestAnimationFrame( animate );
	emotion = document.getElementById('emotion').value;
	if(emotion==="sadness"){
		t+=0.001
		var step = 2*Math.PI / num_bots;
		var i = 0;
		cubes.forEach(cube=>{
			cube.position.x = sad_r*Math.cos(t + i*step) ;
			cube.position.y = sad_r*Math.sin(t + i*step) ;
			cube.rotation.y = Math.atan2( cube.position.y, cube.position.x ) ;
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
		var step = 2*Math.PI / num_bots;
		var i = 0;
		
		for(i=0;i<num_bots;i++){
			
			cubes[i].position.x += arr[i][0]*Math.sin(t + i*Math.PI*0.5);
			cubes[i].position.y += arr[i][1]*Math.sin(t+i*Math.PI*0.5)
			cubes[i].rotation.y = Math.atan2( cubes[i].position.y, cubes[i].position.x ) ;
		};
		
    }
    else if(emotion==="surprise"){
		t+=0.005
		var step = 2*Math.PI / num_bots;
		var i = 0;
		cubes.forEach(cube=>{
			cube.position.x = sur_r*Math.cos(t + i*step) ;
			cube.position.y = sur_r*Math.sin(t + i*step) ;
			cube.rotation.y = Math.atan2( cube.position.y, cube.position.x ) ;
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
		sinx+=0.005
		sinx=sinx%(2*Math.PI);
		var step = 2*Math.PI / num_bots;
		var i = 0;
		cubes.forEach(cube=>{
			cube.position.x = (3+0.5*Math.cos(10*sinx + i*(Math.PI)))*Math.cos(sinx+ i*step);
			cube.position.y = (3+0.5*Math.cos(10*sinx + i*(Math.PI)))*Math.sin(sinx+ i*step);
			cube.rotation.y = Math.atan2( cube.position.y, cube.position.x ) ;
			i += 1;
		});
		 
    }
	
	renderer.render( scene, camera );
}
animate();

