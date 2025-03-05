$fn = 100;

depth = 30;
length = depth * (1+sqrt(5))/2;
height = 20;

inner_ratio = 1-2/(1+sqrt(5));
arch_dist = length/2*(1-inner_ratio-1/30);
arch_height = height/2-height/10;
side_len = length/2 - length*inner_ratio/2;
inset_depth = 0.5;

arch_width = depth/9;
column_w = side_len  - arch_dist;
remaining_len = side_len - column_w - arch_width;

module arch_prism(l, w, h){
    rotate([0,90,0])
    translate([-h,0,0])
    union(){
        translate([w/2,w/2,0])
            cylinder(l, d=w);
        translate([w/2,0,0])
            cube([h - w/2, w, l]);
    }

}

module shell(){
    difference(){
        cube([length,depth,height]);
        translate([side_len,-1,-1])
            cube([length*inner_ratio,depth/2+1,height+2]);
    }
}

module arches(){
    translate([arch_dist,-1,-1])
        rotate([0,0,90])
        arch_prism(depth/2+1, arch_width, arch_height+1);
    translate([arch_dist,-1, height/2])
        rotate([0,0,90])
        arch_prism(depth/2+1, arch_width, arch_height);
    for (i=[0:2]){
        translate([
            arch_dist-arch_width-inset_depth,
            (i+1)*column_w+i*arch_width, 
            height/2
        ])
            arch_prism(depth/2+1, arch_width, arch_height);
        translate([
            arch_dist-arch_width-inset_depth,
            (i+1)*column_w+i*arch_width, 
            -1
        ])
            arch_prism(depth/2+1, arch_width, arch_height+1);
    }
}

module main(){

    difference(){
        shell();
        arches();
 
        translate([remaining_len/4-arch_width/2,-1,arch_height/6])
        cube([arch_width,inset_depth+1,arch_height*2/3]);
        translate([remaining_len*3/4-arch_width/2,-1,arch_height/6])
        cube([arch_width,inset_depth+1,arch_height*2/3]);
        
        translate([remaining_len/4-arch_width/2,-1,arch_height/8+height/2])
        cube([arch_width,inset_depth+1,arch_height*3/4]);
        translate([remaining_len*3/4-arch_width/2,-1,arch_height/8+height/2])
        cube([arch_width,inset_depth+1,arch_height*3/4]);
    }

}
main();




