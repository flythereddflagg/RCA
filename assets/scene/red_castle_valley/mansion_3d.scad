$fn = 100;
golden = (1+sqrt(5))/2;
depth = 30;
length = depth * golden;
height = 20;
inset_depth = 0.5;
detail_out = 0.2;




inner_ratio = 1-1/golden;
arch_dist = length/2*(1-inner_ratio-1/30);
arch_height = height/2-height/10;
side_len = length/2 - length*inner_ratio/2;


arch_width = depth/9;
column_w = side_len  - arch_dist;
remaining_len = side_len - column_w - arch_width;

overhang = 1;
roof_height = height/2/golden;
roof_width = side_len+2*overhang;
roof_len = depth+2*overhang;

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
module window_indents(){
    window_h = arch_height/2*(1-1/golden);
    window_width = arch_width/golden;
    for (i=[0:2]){
        for (j=[0,1]){
            translate([0,0,j*height/2]){
                translate([
                    remaining_len*(i/3+1/6) - window_width/2,
                    -1,
                    window_h
                ])
                     cube([
                        window_width,
                        inset_depth+1,
                        arch_height/(golden)
                    ]);
            }
        }
    }
}
module big_arches(){
    big_arch_width = arch_width * 1.5;
    
    translate([side_len+big_arch_width+column_w,depth/2 - 1,-1])
        rotate([0,0,90])
        arch_prism(depth/2-1, big_arch_width, arch_height+1);
    translate([length/2 + big_arch_width/2 ,depth/2 - 1,-1])
        rotate([0,0,90])
        arch_prism(depth/2-1, big_arch_width, arch_height+1);
    translate([side_len,depth/2 +column_w,-1])
        arch_prism(depth/2-1, big_arch_width, arch_height+1);
    translate([0,0,height/2]){
        translate([side_len+big_arch_width+column_w,depth/2 - 1,0])
            rotate([0,0,90])
            arch_prism(depth/2-1, big_arch_width, arch_height);
        translate([length/2 + big_arch_width/2 ,depth/2 - 1,0])
            rotate([0,0,90])
            arch_prism(depth/2-1, big_arch_width, arch_height);
        translate([side_len,depth/2 +column_w,0])
            arch_prism(depth/2-1, big_arch_width, arch_height);
    }
}
module side_windows(){        
    translate([0,column_w/2,0]){
        for (i=[0:2]){
            translate([inset_depth-1,i*remaining_len,0])
                rotate([0,0,90])
                window_indents();
        }
    }
}
module edge(){
    translate([1-detail_out,-detail_out,height/2])
            rotate([0,0,90])
            cube([depth+2*detail_out,1,detail_out]);
    translate([-detail_out,-detail_out,height/2])
            cube([side_len+2*detail_out,1,detail_out]);
    translate([side_len+detail_out,-detail_out,height/2])
            rotate([0,0,90])
            cube([side_len+2*detail_out,1,detail_out]);
    translate([side_len-detail_out,depth/2-detail_out,height/2])
            cube([side_len+2*detail_out,1,detail_out]);

}
module fence(){
    fence_h = 2;
    for (i=[0:2]){
        translate([column_w*(2+i),column_w/3,0])
            cylinder(h=2, d=column_w*2/3);
    }
    translate([column_w,0,fence_h])
            cube([arch_width,column_w*2/3,detail_out]);
}
module fences(){
    translate([side_len - column_w*2-arch_width,0,height/2])
        fence();
    for (i=[0:2]){
        translate([side_len,i*(arch_width+column_w),height/2])
            rotate([0,0,90])
            fence();
    }
}
module triangular_prism(b, h, l){

    resize([l,b,h])
    translate([1,0.433015,1/4])
    rotate([0,-90,0])
    cylinder(d=1, h=1,$fn=3);
}
module roof_shape(roof_width, roof_height, roof_len){
    roof_angle = atan(roof_height/(roof_width/2));
    difference(){
        triangular_prism(roof_width, roof_height, roof_len);
        rotate([0,-roof_angle,0])
            triangular_prism(roof_width, roof_height, roof_len);
        translate([roof_len,roof_width,0])
        rotate([0,-roof_angle,180])
            triangular_prism(roof_width, roof_height, roof_len);
    }
}
module roof(){
    union(){
    translate([side_len+overhang,-overhang,height])
        rotate([0,0,90])
        roof_shape(roof_width, roof_height, roof_len);
    translate([-overhang,depth-roof_width+overhang,height])

        roof_shape(roof_width, roof_height, length);
    }
}
module floor3(){
    window_w = arch_width/2;
    window_h = arch_height/2;
    window_bottom = height/4;
    gap = 2*column_w;
    floor_start = side_len/2;
    floor_pushback = depth*5/8;
    middle_window = length/2 - window_w/2 - floor_start;
    roof3_w = depth/3;
    translate([floor_start,floor_pushback,height])
        difference(){
            cube([length/2,roof3_w,height/2]);
            translate([middle_window,-1,window_bottom])
                cube([window_w,detail_out+1,window_h]);
            for (i=[0:2]){
                translate([i*(middle_window - gap)/3+gap,-1,window_bottom])
                    cube([window_w,detail_out+1,window_h]);
            }
        }
    translate([floor_start-overhang,floor_pushback-overhang,height*1.5])
        roof_shape(roof3_w+2*overhang, roof_height, length);
}
module west_half(){
    difference(){
    union(){
        difference(){
            shell();
            arches();
            window_indents();
            big_arches();
            side_windows();
        }
        edge();
        fences();
        roof();
        floor3();
    }
    translate([length/2,-5,-5])
            cube([length+10,depth+10,height*5]);
   
}
}

module main(){
    translate([length/2,0,0])
    union(){
    translate([-length/2,0,0])
        west_half();
    mirror([1,0,0])
    translate([-length/2,0,0])
        west_half();
    }


}
main();




