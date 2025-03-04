length = 45;
depth = 30;
height = 20;
$fn = 100;
module arch_prism(h, w, l){
    rotate([0,90,0])
    translate([-h,0,0])
    union(){
        translate([w/2,w/2,0])
            cylinder(l, d=w);
        translate([w/2,0,0])
            cube([h - w/2, w, l]);
    }

}

module arches_windows_upper(){
    magic_constant = (1/9-1/3 + 1/9*0.85*3)/3/2;
    gap = length * magic_constant;
    translate([length/3-gap*1.5,-1,0])
        rotate([0,0,90])
        arch_prism(
            height/2*0.85, 
            length/9*0.7, 
            depth*3/4+1
        );
    translate([length*4/9-gap,-1,0])
        rotate([0,0,90])
        arch_prism(
            height/2*0.85, 
            length/9*0.85, 
            depth*6/9+1
        );
        
    translate([length*5/9-gap,-1,0])
        rotate([0,0,90])
        arch_prism(
            height/2*0.85, 
            length/9*0.85, 
            depth*3/4+1
        );
    for (i=[0:3]){
        translate([length*2/9,i*depth/6+gap,0])
            rotate([0,0,0])
            arch_prism(
                height/2*0.85, 
                length/9*0.85, 
                depth/2+1
            );
    }
    for (i=[0:1]){
        translate([i*length/9+gap,-1,1])
            cube([length/9*0.85,1/2+1,height/4+1.5]);

    }
}



module arches_windows(){
    magic_constant = (1/9-1/3 + 1/9*0.85*3)/3/2;
    gap = length * magic_constant;
    translate([length/3-gap*1.5,-1,-1])
        rotate([0,0,90])
        arch_prism(
            height/2*0.85+1, 
            length/9*0.7, 
            depth*3/4+1
        );
    translate([length*4/9-gap,-1,-1])
        rotate([0,0,90])
        arch_prism(
            height/2*0.85+2, 
            length/9*0.85, 
            depth*6/9+1
        );
        
    translate([length*5/9-gap,-1,-1])
        rotate([0,0,90])
        arch_prism(
            height/2*0.85+2, 
            length/9*0.85, 
            depth*3/4+1
        );
    for (i=[0:3]){
        translate([length*2/9,i*depth/6+gap,-1])
            rotate([0,0,0])
            arch_prism(
                height/2*0.85+1, 
                length/9*0.85, 
                depth/2+1
            );
    }
    for (i=[0:1]){
        translate([i*length/9+gap,-1,2])
            cube([length/9*0.85,1/2+1,height/4]);

    }
}
module main(){
    difference(){
        cube([length,depth,height]);
        translate([length/3,-1,-1])
            cube([length/3,depth/2+1,height+2]);
        arches_windows();
        translate([0,0,height/2])
            arches_windows_upper();
    }
    translate([-0.1,-0.2,height/2])
        cube([length/3+0.2,1,.2]);
    translate([0.8,-0.2,height/2])
        rotate([0,0,90])
        cube([depth+0.2,1,.2]);
    translate([length/3+0.2,-0.2,height/2])
        rotate([0,0,90])
        cube([depth/2+0.2,1,.2]);
    translate([-0.1+length/3,-0.2+depth/2,height/2])
        cube([length/3+0.2,1,.2]);
}
main();
//arch_prism(10, 10, 10);



