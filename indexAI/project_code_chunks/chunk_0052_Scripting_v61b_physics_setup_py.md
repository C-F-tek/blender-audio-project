# Project Code Chunk 52/212

- File: `Scripting/v61b/physics_setup.py`
- Part: `3`
- Lines: `615-737`

## Symbol Map
- Imports: `bpy`, `math`, `random`, `from config import USE_PHYSICS_ACCENTS, PHYSICS_ACCENT_COUNT, PRIMARY_BASE_Z, TURB_STRENGTH_MIN, VORTEX_STRENGTH_MIN, PHYSICS_ORBIT_RADIUS_MIN, PHYSICS_ORBIT_RADIUS_MAX, PHYSICS_ATOM_ORBIT_SPEED_MIN, PHYSICS_ATOM_ORBIT_SPEED_MAX, PHYSICS_ATOM_MICRO_WOBBLE, HERO_GRAVITY_STRENGTH_MIN, TETHER_SPRING_STIFFNESS, TETHER_SPRING_DAMPING, USE_RHYTHM_PARTICLE_PHYSICS, RHYTHM_PARTICLE_COUNT, RHYTHM_DUST_PARTICLE_COUNT, RHYTHM_STREAK_PARTICLE_COUNT, RHYTHM_PARTICLE_LIFETIME, RHYTHM_DUST_LIFETIME, RHYTHM_PARTICLE_EMITTER_RADIUS, RHYTHM_PARTICLE_EMITTER_Z, PARTICLE_SOURCE_LOCATION, RHYTHM_PARTICLE_SOURCE_RADIUS, RHYTHM_PARTICLE_SIZE_MIN, RHYTHM_PARTICLE_NORMAL_MIN, RHYTHM_PARTICLE_TANGENT_MIN, RHYTHM_PARTICLE_BROWNIAN_MIN, USE_ALBUM_LETTER_PARTICLES, ALBUM_PARTICLE_TEXT, ALBUM_LETTER_PARTICLE_COUNT, ALBUM_LETTER_PARTICLE_LIFETIME, ALBUM_LETTER_SOURCE_SIZE, ALBUM_LETTER_EXTRUDE, ALBUM_LETTER_EMISSION_STRENGTH, ALBUM_LETTER_PARTICLE_SIZE_MIN, PHYSICS_ACCENT_EMISSION_MIN, PHYSICS_ACCENT_MIX_MIN, PALETTE_LIST, PEACE_PALETTE`, `from materials import build_variant_material`, `from scene_utils import deselect_all, safe_active`
- Functions: `set_if_available(obj, attr, value)` line 50; `build_particle_emission_material(name, color, strength)` line 60; `build_invisible_emitter_material()` line 82; `get_material_node_socket(material, node_name, socket_name, is_output)` line 106; `add_particle_collision(obj)` line 121; `add_passive_rigidbody(obj)` line 138; `add_active_rigidbody(obj, mass)` line 147; `create_hidden_anchor(name, location)` line 159; `create_spring_constraint(name, object1, object2, location)` line 172; `create_particle_instance(name, color, strength, shape)` line 215; `create_album_letter_particle_collection(parent)` line 255; `create_particle_emitter(name, kind, invisible_mat)` line 339; `configure_particle_system(emitter, name, instance_obj, count, lifetime, particle_size, normal_factor, tangent_factor, brownian_factor, damping, child_count, child_percent, instance_collection)` line 367; `create_rhythm_particle_physics(parent)` line 445; `create_physics_accents(parent)` line 606

## Content
```py
00615:             "accents": [],
00616:             "force_obj": None,
00617:             "turb_obj": None,
00618:             "vortex_obj": None,
00619:             "wind_left": None,
00620:             "wind_right": None,
00621:             "rhythm_particles": rhythm_particles,
00622:         }
00623: 
00624:     accents = []
00625: 
00626:     if floor:
00627:         add_passive_rigidbody(floor)
00628: 
00629:     bpy.ops.object.effector_add(type='FORCE', location=(0, 0, PRIMARY_BASE_Z + 1.20))
00630:     force_obj = bpy.context.active_object
00631:     force_obj.name = "HeroGravityField"
00632:     force_obj.field.strength = -HERO_GRAVITY_STRENGTH_MIN
00633:     force_obj.field.flow = 1.0
00634:     force_obj.field.noise = 0.10
00635:     force_obj.field.falloff_power = 1.55
00636: 
00637:     bpy.ops.object.effector_add(type='TURBULENCE', location=(0, 0, PRIMARY_BASE_Z + 1.50))
00638:     turb_obj = bpy.context.active_object
00639:     turb_obj.name = "AtmosphereTurbulence"
00640:     turb_obj.field.strength = TURB_STRENGTH_MIN
00641:     turb_obj.field.size = 2.0
00642:     turb_obj.field.flow = 0.45
00643: 
00644:     bpy.ops.object.effector_add(type='VORTEX', location=(0, 0, PRIMARY_BASE_Z + 1.00))
00645:     vortex_obj = bpy.context.active_object
00646:     vortex_obj.name = "OrbitVortex"
00647:     vortex_obj.rotation_euler.x = math.radians(90.0)
00648:     vortex_obj.field.strength = VORTEX_STRENGTH_MIN
00649: 
00650:     bpy.ops.object.effector_add(type='WIND', location=(-3.0, -1.2, PRIMARY_BASE_Z + 1.8))
00651:     wind_left = bpy.context.active_object
00652:     wind_left.name = "WindLeft"
00653:     wind_left.rotation_euler = (math.radians(90), 0, math.radians(20))
00654:     wind_left.field.strength = 0.0
00655:     wind_left.field.flow = 1.0
00656: 
00657:     bpy.ops.object.effector_add(type='WIND', location=(3.0, -1.2, PRIMARY_BASE_Z + 1.8))
00658:     wind_right = bpy.context.active_object
00659:     wind_right.name = "WindRight"
00660:     wind_right.rotation_euler = (math.radians(90), 0, math.radians(-20))
00661:     wind_right.field.strength = 0.0
00662:     wind_right.field.flow = 1.0
00663: 
00664:     radius_span = max(0.01, PHYSICS_ORBIT_RADIUS_MAX - PHYSICS_ORBIT_RADIUS_MIN)
00665:     for i in range(PHYSICS_ACCENT_COUNT):
00666:         shell_t = (i % 6) / 5.0
00667:         radius = PHYSICS_ORBIT_RADIUS_MIN + radius_span * shell_t + random.uniform(-0.08, 0.10)
00668:         angle = (i / max(1, PHYSICS_ACCENT_COUNT)) * math.tau + random.uniform(-0.18, 0.18)
00669:         z_offset = random.uniform(-0.52, 0.88)
00670:         z = PRIMARY_BASE_Z + 1.02 + z_offset
00671: 
00672:         x = math.cos(angle) * radius
00673:         y = math.sin(angle) * radius
00674:         loc = (x, y, z)
00675: 
00676:         color = PALETTE_LIST[i % len(PALETTE_LIST)]
00677: 
00678:         anchor = create_hidden_anchor(f"PhysicsAnchor_{i:02d}", loc)
00679: 
00680:         bpy.ops.mesh.primitive_uv_sphere_add(
00681:             radius=random.uniform(0.07, 0.12),
00682:             location=loc,
00683:         )
00684:         obj = bpy.context.active_object
00685:         obj.name = f"PhysicsAccent_{i:02d}"
00686: 
00687:         mat = build_variant_material(f"PhysicsAccentMat_{i:02d}", color)
00688:         emit_socket = get_material_node_socket(mat, "VariantEmission", "Strength")
00689:         mix_socket = get_material_node_socket(mat, "VariantEmissionMix", 0, is_output=True)
00690:         if emit_socket is not None:
00691:             emit_socket.default_value = PHYSICS_ACCENT_EMISSION_MIN
00692:         if mix_socket is not None:
00693:             mix_socket.default_value = PHYSICS_ACCENT_MIX_MIN
00694:         obj.data.materials.append(mat)
00695: 
00696:         add_active_rigidbody(obj, mass=0.14)
00697:         try:
00698:             obj.rigid_body.kinematic = True
00699:         except Exception:
00700:             pass
00701: 
00702:         constraint = create_spring_constraint(
00703:             f"PhysicsSpring_{i:02d}",
00704:             anchor,
00705:             obj,
00706:             loc,
00707:         )
00708: 
00709:         accents.append({
00710:             "object": obj,
00711:             "anchor": anchor,
00712:             "constraint": constraint,
00713:             "base_location": obj.location.copy(),
00714:             "base_rotation": obj.rotation_euler.copy(),
00715:             "phase": random.uniform(0.0, math.tau),
00716:             "orbit_radius": radius,
00717:             "orbit_angle": angle,
00718:             "orbit_z_offset": z_offset,
00719:             "orbit_speed": random.uniform(PHYSICS_ATOM_ORBIT_SPEED_MIN, PHYSICS_ATOM_ORBIT_SPEED_MAX),
00720:             "orbit_tilt": random.uniform(-0.42, 0.42),
00721:             "micro_radius": random.uniform(PHYSICS_ATOM_MICRO_WOBBLE * 0.45, PHYSICS_ATOM_MICRO_WOBBLE * 1.25),
00722:             "band": ["low", "mid", "high", "beat", "onset"][i % 5],
00723:             "response": random.uniform(0.42, 1.0),
00724:             "emission_socket": emit_socket,
00725:             "mix_socket": mix_socket,
00726:             "material": mat,
00727:         })
00728: 
00729:     return {
00730:         "accents": accents,
00731:         "force_obj": force_obj,
00732:         "turb_obj": turb_obj,
00733:         "vortex_obj": vortex_obj,
00734:         "wind_left": wind_left,
00735:         "wind_right": wind_right,
00736:         "rhythm_particles": rhythm_particles,
00737:     }
```
