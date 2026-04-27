# Project Code Chunk 103/212

- File: `Scripting/v61b_backgood/physics_setup.py`
- Part: `3`
- Lines: `615-720`

## Symbol Map
- Imports: `bpy`, `math`, `random`, `from config import USE_PHYSICS_ACCENTS, PHYSICS_ACCENT_COUNT, PRIMARY_BASE_Z, TURB_STRENGTH_MIN, VORTEX_STRENGTH_MIN, PHYSICS_ORBIT_RADIUS_MIN, PHYSICS_ORBIT_RADIUS_MAX, TETHER_SPRING_STIFFNESS, TETHER_SPRING_DAMPING, USE_RHYTHM_PARTICLE_PHYSICS, RHYTHM_PARTICLE_COUNT, RHYTHM_DUST_PARTICLE_COUNT, RHYTHM_STREAK_PARTICLE_COUNT, RHYTHM_PARTICLE_LIFETIME, RHYTHM_DUST_LIFETIME, RHYTHM_PARTICLE_EMITTER_RADIUS, RHYTHM_PARTICLE_EMITTER_Z, PARTICLE_SOURCE_LOCATION, RHYTHM_PARTICLE_SOURCE_RADIUS, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_BROWNIAN_MIN, USE_ALBUM_LETTER_PARTICLES, ALBUM_PARTICLE_TEXT, ALBUM_LETTER_PARTICLE_COUNT, ALBUM_LETTER_PARTICLE_LIFETIME, ALBUM_LETTER_SOURCE_SIZE, ALBUM_LETTER_EXTRUDE, ALBUM_LETTER_EMISSION_STRENGTH, ALBUM_LETTER_PARTICLE_SIZE_MIN, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_MIX_MIN, PALETTE_LIST, PEACE_PALETTE`, `from materials import build_variant_material`, `from scene_utils import deselect_all, safe_active`
- Functions: `set_if_available(obj, attr, value)` line 46; `build_particle_emission_material(name, color, strength)` line 56; `build_invisible_emitter_material()` line 78; `get_material_node_socket(material, node_name, socket_name, is_output)` line 102; `add_particle_collision(obj)` line 117; `add_passive_rigidbody(obj)` line 134; `add_active_rigidbody(obj, mass)` line 143; `create_hidden_anchor(name, location)` line 155; `create_spring_constraint(name, object1, object2, location)` line 168; `create_particle_instance(name, color, strength, shape)` line 211; `create_album_letter_particle_collection(parent)` line 251; `create_particle_emitter(name, kind, invisible_mat)` line 335; `configure_particle_system(emitter, name, instance_obj, count, lifetime, particle_size, normal_factor, tangent_factor, brownian_factor, damping, child_count, child_percent, instance_collection)` line 363; `create_rhythm_particle_physics(parent)` line 441; `create_physics_accents(parent)` line 602

## Content
```py
00615:             "wind_left": None,
00616:             "wind_right": None,
00617:             "rhythm_particles": rhythm_particles,
00618:         }
00619: 
00620:     accents = []
00621: 
00622:     if floor:
00623:         add_passive_rigidbody(floor)
00624: 
00625:     bpy.ops.object.effector_add(type='FORCE', location=(0, 0, PRIMARY_BASE_Z + 1.20))
00626:     force_obj = bpy.context.active_object
00627:     force_obj.name = "PulseForceField"
00628:     force_obj.field.strength = 0.0
00629:     force_obj.field.flow = 1.0
00630:     force_obj.field.noise = 0.30
00631:     force_obj.field.falloff_power = 2.0
00632: 
00633:     bpy.ops.object.effector_add(type='TURBULENCE', location=(0, 0, PRIMARY_BASE_Z + 1.50))
00634:     turb_obj = bpy.context.active_object
00635:     turb_obj.name = "AtmosphereTurbulence"
00636:     turb_obj.field.strength = TURB_STRENGTH_MIN
00637:     turb_obj.field.size = 2.0
00638:     turb_obj.field.flow = 0.45
00639: 
00640:     bpy.ops.object.effector_add(type='VORTEX', location=(0, 0, PRIMARY_BASE_Z + 1.00))
00641:     vortex_obj = bpy.context.active_object
00642:     vortex_obj.name = "OrbitVortex"
00643:     vortex_obj.rotation_euler.x = math.radians(90.0)
00644:     vortex_obj.field.strength = VORTEX_STRENGTH_MIN
00645: 
00646:     bpy.ops.object.effector_add(type='WIND', location=(-3.0, -1.2, PRIMARY_BASE_Z + 1.8))
00647:     wind_left = bpy.context.active_object
00648:     wind_left.name = "WindLeft"
00649:     wind_left.rotation_euler = (math.radians(90), 0, math.radians(20))
00650:     wind_left.field.strength = 0.0
00651:     wind_left.field.flow = 1.0
00652: 
00653:     bpy.ops.object.effector_add(type='WIND', location=(3.0, -1.2, PRIMARY_BASE_Z + 1.8))
00654:     wind_right = bpy.context.active_object
00655:     wind_right.name = "WindRight"
00656:     wind_right.rotation_euler = (math.radians(90), 0, math.radians(-20))
00657:     wind_right.field.strength = 0.0
00658:     wind_right.field.flow = 1.0
00659: 
00660:     for i in range(PHYSICS_ACCENT_COUNT):
00661:         radius = random.uniform(PHYSICS_ORBIT_RADIUS_MIN, PHYSICS_ORBIT_RADIUS_MAX)
00662:         angle = random.uniform(0.0, math.tau)
00663:         z = random.uniform(PRIMARY_BASE_Z + 0.10, PRIMARY_BASE_Z + 1.70)
00664: 
00665:         x = math.cos(angle) * radius
00666:         y = math.sin(angle) * radius
00667:         loc = (x, y, z)
00668: 
00669:         color = PALETTE_LIST[i % len(PALETTE_LIST)]
00670: 
00671:         anchor = create_hidden_anchor(f"PhysicsAnchor_{i:02d}", loc)
00672: 
00673:         bpy.ops.mesh.primitive_uv_sphere_add(
00674:             radius=random.uniform(0.07, 0.12),
00675:             location=loc,
00676:         )
00677:         obj = bpy.context.active_object
00678:         obj.name = f"PhysicsAccent_{i:02d}"
00679: 
00680:         mat = build_variant_material(f"PhysicsAccentMat_{i:02d}", color)
00681:         emit_socket = get_material_node_socket(mat, "VariantEmission", "Strength")
00682:         mix_socket = get_material_node_socket(mat, "VariantEmissionMix", 0, is_output=True)
00683:         if emit_socket is not None:
00684:             emit_socket.default_value = PHYSICS_ACCENT_EMISSION_MIN
00685:         if mix_socket is not None:
00686:             mix_socket.default_value = PHYSICS_ACCENT_MIX_MIN
00687:         obj.data.materials.append(mat)
00688: 
00689:         add_active_rigidbody(obj, mass=0.14)
00690: 
00691:         constraint = create_spring_constraint(
00692:             f"PhysicsSpring_{i:02d}",
00693:             anchor,
00694:             obj,
00695:             loc,
00696:         )
00697: 
00698:         accents.append({
00699:             "object": obj,
00700:             "anchor": anchor,
00701:             "constraint": constraint,
00702:             "base_location": obj.location.copy(),
00703:             "base_rotation": obj.rotation_euler.copy(),
00704:             "phase": random.uniform(0.0, math.tau),
00705:             "band": ["low", "mid", "high", "beat", "onset"][i % 5],
00706:             "response": random.uniform(0.42, 1.0),
00707:             "emission_socket": emit_socket,
00708:             "mix_socket": mix_socket,
00709:             "material": mat,
00710:         })
00711: 
00712:     return {
00713:         "accents": accents,
00714:         "force_obj": force_obj,
00715:         "turb_obj": turb_obj,
00716:         "vortex_obj": vortex_obj,
00717:         "wind_left": wind_left,
00718:         "wind_right": wind_right,
00719:         "rhythm_particles": rhythm_particles,
00720:     }
```
