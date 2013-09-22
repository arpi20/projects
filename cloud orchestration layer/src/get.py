from uuid import uuid4
import json
query=[]
volquery=[]
machines_list=[]
def get_machines(filename):
	lines=[line.strip() for line in open(filename)]
	for line in lines:
		machine=line.split("@")
		machines_list.append(machine + [str(uuid4())])

image_list=[]
def get_images(filename):
	lines=[line.strip() for line in open(filename)]
	for line in lines:
		image_list.append(line)
	

def get_xml(vm_name,domain_type,uuid,user,image_id,cpu,ram,emulator_path):
			

        xml=r"<domain type='qemu' id='"+domain_type+r"'>\
      <name>"+vm_name+r"</name>\
      <memory>"+str((ram*1024))+r"</memory>\
      <vcpu>"+cpu+r"</vcpu>\
      <os>\
        <type arch='x86_64' machine='pc-1.0'>hvm</type>\
        <boot dev='hd'/>\
      </os>\
      <features>\
        <acpi/>\
        <apic/>\
        <pae/>\
      </features>\
      <clock offset='utc'/>\
      <on_poweroff>destroy</on_poweroff>\
      <on_reboot>restart</on_reboot>\
      <on_crash>restart</on_crash>\
      <devices>\
        <emulator>/usr/bin/qemu-system-x86_64</emulator>\
        <disk type='file' device='disk'>\
          <driver name='qemu' type='raw'/>\
          <source file='/home/"+user+r"/"+image_id+r".img'/>\
          <target dev='hda' bus='ide'/>\
          <alias name='ide0-0-0'/>\
          <address type='drive' controller='0' bus='0' unit='0'/>\
        </disk>\
        <controller type='ide' index='0'>\
          <alias name='ide0'/>\
          <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>\
        </controller>\
        <serial type='pty'>\
          <source path='/dev/pts/2'/>\
          <target port='0'/>\
          <alias name='serial0'/>\
        </serial>\
        <console type='pty' tty='/dev/pts/2'>\
          <source path='/dev/pts/2'/>\
          <target type='serial' port='0'/>\
          <alias name='serial0'/>\
        </console>\
        <input type='mouse' bus='ps2'/>\
        <graphics type='vnc' port='5900' autoport='yes'/>\
        <sound model='ich6'>\
          <alias name='sound0'/>\
          <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>\
        </sound>\
        <video>\
          <model type='cirrus' vram='9216' heads='1'/>\
          <alias name='video0'/>\
          <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>\
        </video>\
        <memballoon model='virtio'>\
          <alias name='balloon0'/>\
          <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>\
        </memballoon>\
      </devices>\
      <seclabel type='dynamic' model='apparmor' relabel='yes'>\
        <label>libvirt-10a963ef-9458-c30d-eca3-891efd2d5817</label>\
        <imagelabel>libvirt-10a963ef-9458-c30d-eca3-891efd2d5817</imagelabel>\
      </seclabel>\
    </domain>"

		
	return xml 


def get_diskxml(hostname,poolname):
	xml="<disk type='network' device='disk'> \
                <source protocol='rbd' name='rbd/"+poolname+r"'>\
                        <host name='"+hostname+r"' port='6789'/>\
                </source>\
                <target dev='hdb' bus='scsi'/>\
                </disk>	"
	return xml



def image_copy_onsys(image,image_id):
	global image_name
	imgname=image_name[image_id-1]
	copy_image="scp "+image+" "+" ~/"+imgname+".img"
	return copy_image

def image_copy_fromsys(user,ip,image_id):
	global image_name
	imgname=image_name[image_id-1]
	copy_image="scp ~/"+imgname+".img "+user+"@"+ip+":~/"+imgname+".img"
	return copy_image
	

def make_path(user,ip):
	path = 'remote+ssh://' + user + '@' + ip + '/' 
	return path

machine_num=-1
def pick_machine():
	global machine_num
	machine_num=machine_num+1
	machine_num=machine_num%len(machines_list)
	return machine_num

vmid_num=0
def getvmid_num():
	global vmid_num
	vmid_num=vmid_num+1
	return vmid_num

volid_num=0
def getvolid_num():
	global volid_num
	volid_num=volid_num+1
	return volid_num

data={}
def parse_vmtype(filename):
	global data
	json_data=open(filename)
	data=json.load(json_data)
	json_data.close()

image_name=[]
def get_imagename():
	global image_list
	for line in image_list:
		image=line.split("/")
		image=image[-1].split(".")
		image_name.append(image[0])
	


	
