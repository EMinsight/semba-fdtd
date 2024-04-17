from utils import *

def test_read_wire_probe():
    p = Probe(OUTPUT_FOLDER + 'holland1981.fdtd_mid_point_Wz_11_11_12_s2.dat')
        
    assert p.case_name == 'holland1981'
    assert p.name == 'mid_point'
    assert p.type == 'wire'
    assert np.all(p.cell == np.array([11, 11, 12]))
    assert p.segment_tag == 2
    
    assert len(p['time']) == 1001
    assert p['time'][0] == 0.0
    assert p['time'].iat[-1] == 0.99999999600419720E-009
    
    assert len(p['current']) == 1001
    assert p['current'][0] == 0.0
    assert p['current'].iat[-1] == -0.228888888E-021
  

def test_probes_output_exists(tmp_path):
    case = 'holland1981'
    input_json = getCase(case)
    input_json['general']['numberOfSteps'] = 1
    fn = tmp_path._str + '/' + case + '.fdtd.json'
    with open(fn, 'w') as modified_json:
        json.dump(input_json, modified_json) 

    makeCopy(tmp_path, EXCITATIONS_FOLDER+'gauss.exc')

    solver = FDTD(input_filename = fn, path_to_exe=SEMBA_EXE)
    solver.run()
    probe_files = solver.getSolvedProbeFilenames("mid_point")
    
    assert solver.hasFinishedSuccessfully() == True
    assert len(probe_files) == 1
    assert 'holland1981.fdtd_mid_point_Wz_11_11_12_s2.dat' == probe_files[0]     
    


def test_probes_output_number_of_steps(tmp_path):
    case = 'holland1981'
    input_json = getCase(case)
    number_of_steps = 10
    input_json['general']['numberOfSteps'] = number_of_steps
    fn = tmp_path._str + '/' + case + '.fdtd.json'
    with open(fn, 'w') as modified_json:
        json.dump(input_json, modified_json) 

    makeCopy(tmp_path, EXCITATIONS_FOLDER+'gauss.exc')

    solver = FDTD(input_filename = fn, path_to_exe=SEMBA_EXE)
    solver.run()
    probe_files = solver.getSolvedProbeFilenames("mid_point")
    
    assert solver.hasFinishedSuccessfully() == True
    assert len(probe_files) == 1
    assert 'holland1981.fdtd_mid_point_Wz_11_11_12_s2.dat' == probe_files[0]
    assert countLinesInFile(probe_files[0]) == number_of_steps + 2

def test_holland(tmp_path):
    case = 'holland1981'
    makeTemporaryCopy(tmp_path, EXCITATIONS_FOLDER+'gauss.exc')
    makeTemporaryCopy(tmp_path, CASE_FOLDER + case + '.fdtd.json')
    fn = tmp_path._str + '/' + case + '.fdtd.json'

    solver = FDTD(input_filename = fn, path_to_exe=SEMBA_EXE)
    solver.run()
    probe_files = solver.getSolvedProbeFilenames("mid_point")
    
    assert solver.hasFinishedSuccessfully() == True
    assert len(probe_files) == 1
    assert 'holland1981.fdtd_mid_point_Wz_11_11_12_s2.dat' == probe_files[0]
    assert countLinesInFile(probe_files[0]) == 1002
    # assert compareFiles(OUTPUT_FOLDER+'holland1981.fdtd_mid_point_Wz_11_11_12_s2.dat',\
    #                     probe_files[0])


    
def test_towel_hanger(tmp_path):
    case = 'towelHanger'
    input_json = getCase(case)
    input_json['general']['numberOfSteps'] = 1
    # input_json['general']['timeStep'] = 3.0E-013
    
    fn = tmp_path._str + '/' + case + '.fdtd.json'
    with open(fn, 'w') as modified_json:
        json.dump(input_json, modified_json) 

    makeCopy(tmp_path, EXCITATIONS_FOLDER+'ramp.exc')

    solver = FDTD(input_filename = fn, path_to_exe=SEMBA_EXE)
    solver.run()
    probe_start = solver.getSolvedProbeFilenames("wire_start")
    probe_end = solver.getSolvedProbeFilenames("wire_end")
    
    assert solver.hasFinishedSuccessfully() == True
    assert len(probe_start) == 1
    assert len(probe_end) == 1
    
    assert 'towelHanger.fdtd_wire_start_Wz_27_25_30_s1.dat' == probe_start[0]
    assert 'towelHanger.fdtd_wire_end_Wz_43_25_30_s4.dat' == probe_end[0]
    assert countLinesInFile(probe_start[0]) == 3
    assert countLinesInFile(probe_end[0]) == 3
    # assert compareFiles(solver.wd+OUTPUT_FOLDER+'towelHanger.fdtd_wire_end_Wz_100_100_80_s4.dat',\
    #                     probe_files[0])
   
        
def test_read_far_field_probe(tmp_path):    
    case = 'sphere'
    input_json = getCase(case)
    input_json['general']['numberOfSteps'] = 1
    input_json['probes'][0]['domain']['numberOfFrequencies'] = 100
    
    
    fn = tmp_path._str + '/' + case + '.fdtd.json'
    with open(fn, 'w') as modified_json:
        json.dump(input_json, modified_json) 

    makeCopy(tmp_path, EXCITATIONS_FOLDER+'gauss.exc')

    solver = FDTD(input_filename = fn, path_to_exe=SEMBA_EXE)
    solver.run()  
    probe_files = solver.getSolvedProbeFilenames("Far") # semba-fdtd seems to always use the name Far for "far field" probes.

    probe_files = solver.getSolvedProbeFilenames("Far")
    p_ff = Probe(probe_files[0])
    
    assert p_ff.case_name == 'sphere'
    assert p_ff.type == 'farField'
    assert np.all(p_ff.cell_init == np.array([2,2,2]))
