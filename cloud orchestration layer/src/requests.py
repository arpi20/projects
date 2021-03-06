from flask import Flask,request,render_template,Blueprint,session,jsonify
import get
import libvirt,os,subprocess

server=Blueprint('requests', __name__)
@server.route('/vm/create/',methods=['GET'])
def req_create():
	try:
		vm_name=request.args.get('name')
		instance_type=int(request.args.get('instance_type'))
		image_id=int(request.args.get('image_id'))

		cpu_required=int(get.data['types'][instance_type-1]['cpu'])
		ram_required=int(get.data['types'][instance_type-1]['ram'])
		
		image=get.image_list[image_id-1]
		req_proc_bit=get.image_name[image_id-1].split("amd")
		req_proc_bit=int(req_proc_bit[1])

		pmid=get.pick_machine()
		machine=get.machines_list[pmid]
		user=machine[0]
		ip=machine[1]
		uuid=machine[2]
		
		try:
			check=subprocess.check_output("ssh "+user+"@"+ip+" cat /proc/cpuinfo | grep lm",shell=True)
			avail_proc_bit=64
		except:
			avail_proc_bit=32


		available_cpu=int(subprocess.check_output("ssh "+user+"@"+ip+" nproc",shell=True))
		free_space=subprocess.check_output("ssh "+user+"@"+ip+" free -m",shell=True)
		free_space=free_space.split("\n")
		free_space=free_space[1].split()
		available_ram=int(free_space[3])


		while(available_cpu<cpu_required or available_ram<ram_required or avail_proc_bit<req_proc_bit):
			pmid=get.pick_machine()
			if pmid==0:
				return jsonify(Error="cpu in machines are not compatible with instance type")
			machine=get.machines_list[pmid]
			user=machine[0]
			ip=machine[1]
			uuid=machine[2]
			
			try:
				check=subprocess.check_output("ssh "+user+"@"+ip+" cat /proc/cpuinfo | grep lm",shell=True)
				avail_proc_bit=64
			except:
				avail_proc_bit=32


			available_cpu=int(subprocess.check_output("ssh "+user+"@"+ip+" nproc",shell=True))
			free_space=subprocess.check_output("ssh "+user+"@"+ip+" free -m",shell=True)
			free_space=free_space.split("\n")
			free_space=free_space[1].split()
			available_ram=int(free_space[3])
			

		
		os.system(get.image_copy_onsys(image,image_id))
		os.system(get.image_copy_fromsys(user,ip,image_id))
		
		
		conn=libvirt.open(get.make_path(user,ip))
		capa=conn.getCapabilities()
		emulator_path = capa.split("emulator>")
		emulator_path = emulator_path[1].split("<")[0] #location of xen/qemu
		req=conn.defineXML(get.get_xml(vm_name,conn.getType().lower(),uuid,user,str(image_id),str(cpu_required),ram_required,emulator_path))
		try:
			req.create()
		except:
			return jsonify(vmid=0)
		
		vmid=get.getvmid_num()
		get.query.append(dict(vmid=vmid,name=vm_name,instance_type=instance_type,pmid=pmid))
		return jsonify(vmid=vmid)
	except:
		return jsonify(vmid=0)



@server.route('/vm/query/',methods=['GET'])
def req_query():
	try:
		vmid=int(request.args.get('vmid'))
		vm_info=get.query[vmid-1]
		return jsonify(vmid=vmid,name=vm_info['name'],instance_type=vm_info['instance_type'],pmid=vm_info['pmid'])
	except:
		return jsonify(vmid=0,name=" ",instance_type=0)



@server.route('/vm/destroy/',methods=['GET'])
def req_destroy():
	try:
		vmid=int(request.args.get('vmid'))
		pmid=get.query[vmid-1]['pmid']
		machine=get.machines_list[pmid]
		user=machine[0]
		ip=machine[1]
		conn=libvirt.open(get.make_path(user,ip))
		req=conn.lookupByName(get.query[vmid-1]['name'])
		if req.isActive():
			req.destroy()
		req.undefine()
		del get.query[vmid-1]
		return jsonify(status=1)
	except:
		return jsonify(status=0)
	

@server.route('/vm/types/',methods=['GET'])
def req_types():
	return jsonify(types=get.data["types"])	

@server.route('/image/list/',methods=['GET'])
def req_images():
	out=[]	
	images=get.image_name
	im_id=0
	for image in images:
		im_id=im_id+1
		out.append({"id":im_id,"name":image})
	return jsonify(images=out)

		
@server.route('/volume/create/',methods=['GET'])
def create_vol():
	name=request.args.get('name')	
	size=request.args.get('size')
	try:
		os.system("sudo rbd create "+name+" --size "+ size)
		os.system("sudo modprobe rbd")
		os.system("sudo rbd map "+ name +" --pool rbd --name client.admin")
		vol_num=get.getvolid_num()
		get.volquery.append(dict(volumeid=vol_num,name=name,size=size,status="available",vmid=-1))
		return jsonify(volumeid=vol_num)
	except:
		return jsonify(volumeid=0)


@server.route('/volume/destroy/',methods=['GET'])
def destroy_vol():
	try:
		volid=int(request.args.get('volumeid'))
		os.system("sudo rbd unmap /dev/rbd/rbd/"+get.volquery[volid-1]['name'])
		os.system("sudo rbd rm " + get.volquery[volid-1]['name'])
		del get.volquery[volid-1]
		return jsonify(status=1)
	except:
		return jsonify(status=0)

@server.route('/volume/query/',methods=['GET'])
def query_vol():
	volid=int(request.args.get('volumeid'))
	if volid<=0:	
		return jsonify(error="volumeid: does not exist")
		
	try:	
		vol_info=get.volquery[volid-1]
		if vol_info['status']=="available":
			return jsonify(volumeid=volid,name=vol_info['name'],size=vol_info['size'],status=vol_info['status'])
		if vol_info['status']=="attached":
			return jsonify(volumeid=volid,name=vol_info['name'],size=vol_info['size'],status=vol_info['status'],vmid=vol_info['vmid'])
	
	except:
		return jsonify(error="volumeid: does not exist")

	

@server.route('/volume/attach/',methods=['GET'])
def attach_vol():
	vmid=request.args.get('vmid')
	volid=request.args.get('volumeid')

	vmname=get.query[vmid-1]['name']
	POOL=get.volquery[volid-1]['name']
	Imagename = create_vol.mydir[volid-1]['name']
	HOSTNAME=os.system("hostname")
	connector="qemu+ssh://"+HOSTNAME+"/system"
	
	conn = libvirt.open(connector)
	domain=conn.lookupByName(vmname)
	
	template = get.get_diskxml(HOSTNAME,POOL)
	try:
		domain.attachDevice(template)
		return jsonify(status=1)
	except:
		return jsonify(status=0)
