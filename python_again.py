# -*- coding: utf-8 -*-
from twisted.internet.protocol import DatagramProtocol
from c2w.main.lossy_transport import LossyTransport
from c2w.protocol.udp_chat_server import *
import logging
import struct
logging.basicConfig()
moduleLogger = logging.getLogger('c2w.protocol.udp_chat_client_protocol')
class c2wUdpChatClientProtocol(DatagramProtocol):
    def __init__(self, serverAddress, serverPort, clientProxy, lossPr):
        """
        :param serverAddress: The IP address (or the name) of the c2w server,
            given by the user.
        :param serverPort: The port number used by the c2w server,
            given by the user.
        :param clientProxy: The clientProxy, which the protocol must use
            to interact with the Graphical User Interface.

        Class implementing the UDP version of the client protocol.

        .. note::
            You must write the implementation of this class.

        Each instance must have at least the following attributes:

        .. attribute:: serverAddress

            The IP address of the c2w server.

        .. attribute:: serverPort

            The port number of the c2w server.

        .. attribute:: clientProxy

            The clientProxy, which the protocol must use
            to interact with the Graphical User Interface.

        .. attribute:: lossPr

            The packet loss probability for outgoing packets.  Do
            not modify this value!  (It is used by startProtocol.)

        .. note::
            You must add attributes and methods to this class in order
            to have a working and complete implementation of the c2w
            protocol.
        """
        #: The IP address of the c2w server.
        self.serverAddress = serverAddress
        #: The port number of the c2w server.
        self.serverPort = serverPort
        #: The clientProxy, which the protocol must use
        #: to interact with the Graphical User Interface.
        self.clientProxy = clientProxy
        self.lossPr = lossPr
        #dictionaire pour les id des films
        self.dictmoovie=dict()
        self.seqnum=0
        self.Token=0
        self.seqgtr=0
        self.deconnexion=4
        self.nombre_envoie=0
        self.reception_ack = {}
    def startProtocol(self):
        """
        DO NOT MODIFY THE FIRST TWO LINES OF THIS METHOD!!

        If in doubt, do not add anything to this method.  Just ignore it.
        It is used to randomly drop outgoing packets if the -l
        command line option is used.
        """
        self.transport = LossyTransport(self.transport, self.lossPr)
        DatagramProtocol.transport = self.transport
    
    
      #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
      #
      #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def numseq(self,seq):
        #on genere un numero de sequence pour chaque paquet envoyé
        # en augmentant la valeur recue pour le prochain paquet
        # une fois le numero de sequence a 65536 on le reinitialise
        if     seq==65536:
               seq=0
        else: 
               seq+=1
        return seq
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
         #
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #si le paquet recu est de type login reponse on teste la valeur de coderep
    def Preparepaquet(self,Version,Type,Token,Sequencenumber,payload):
        payloadsize=len(payload)
        header1=(Version<<28)+(Type<<24)+Token
        header2=(Sequencenumber<<16)+payloadsize
        packet=struct.pack('>II'+str(len(payload))+'s',header1,header2,payload.encode('utf−8'))
        return(packet)
          
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
         #
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #si le paquet recu est de type login reponse on teste la valeur de coderep
    def PaquetLRQ(self,Version,Type,Token,Sequencenumber,iduser,username):
        usernamepack=struct.pack('>HH'+str(len(username.encode('utf−8')))+'s',iduser,len(username.encode('utf−8')),username.encode('utf−8'))
        userdatasize=len(usernamepack)
        header1=(Version<<28)+(Type<<24)+Token
        header2=(Sequencenumber<<16)+userdatasize
        packet=struct.pack('>II',header1,header2)+usernamepack
        return(packet)
    
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
         #
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #si le paquet recu est de type login reponse on teste la valeur de coderep
                         
    # pour recevoir les paquets simples avec payload non decodé
    def paquetsimple(self, datagram):
        (header1,header2,payload)=struct.unpack('>II'+str(len(datagram)-8)+'s',datagram)
        token=header1 & int('111111111111111111111111',2)
        header1=header1 >> 24 
        Type=header1 & int('1111',2)
        header1=header1 >> 4 
        version=header1
        payloadsize=header2 & int('1111111111111111',2)
        header2=header2 >> 16
        seqnum=header2 & int('1111111111111111',2)
        return(version,Type,token,seqnum,payloadsize,payload)
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
         #
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #si le paquet recu est de type login reponse on teste la valeur de coderep
    
    def paquetrecuLRP(self, datagram):
        (header1,header2,coderp,userid,username)=struct.unpack('>IIBH'+str(len(datagram)-11)+'s',datagram)
        token=header1 & int('111111111111111111111111',2)
        header1=header1 >> 24 
        Type=header1 & int('1111',2)
        header1=header1 >> 4 
        version=header1
        payloadsize=header2 & int('1111111111111111',2)
        header2=header2 >> 16
        seqnum=header2 & int('1111111111111111',2)
        return(version,Type,token,seqnum,payloadsize,coderp,userid,username)
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
         #
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #si le paquet recu est de type login reponse on teste la valeur de coderep
    def constructack(self,Version,Type,Token,Sequencenumber,payload):
        payloadsize=len(payload)
        header1=(Version<<28)+(Type<<24)+Token
        header2=(Sequencenumber<<16)+payloadsize
        packet=struct.pack('>II'+str(len(payload))+'s',header1,header2,payload.encode('utf−8'))
        return(packet)
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
         #
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def paquetGTR(self,Token,Seqnumber,moovie_id):
        header1=(1<<28)+(5<<24)+Token
        payload=struct.pack('>H',moovie_id)
        gtrdatasize=len(payload)
        header2=(Seqnumber<<16)+gtrdatasize
        packet=struct.pack('>II',header1,header2)+payload
        return(packet)
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
         #fonnction de depaquetage lors de la reception de RST
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def depaquetageRST(self,datagram):
        # affiche le rst recu
        print(" ".join("{:02x}".format(c) for c in datagram))
        
         # liste contenant la liste des utilisateurs dans la mainroom
        userList=list()
        # liste contenant le nom, port et l'ip du film
        movieList=list()
         # dictionnaire contenant les id de chaque film en fonction de leur nom
        user_moovielist=dict()
         # liste contenant l'id, port et l'ip du film
        userdata=list()
        datagram=datagram[8:]
        print(datagram)
        id_mainroom=struct.unpack('>H',datagram[0:2])[0]
       
        datagram=datagram[2:]
        taille=struct.unpack('>H',datagram[0:2])[0]
       
        datagram=datagram[2:]
        mainroom=struct.unpack(str(taille)+'s',datagram[0:taille])
        mainroom=mainroom[0].decode('utf-8') 
        mainroom=ROOM_IDS.MAIN_ROOM
        datagram=datagram[taille:]
        # récupere l'adresse ip et le port de la main room
        ip=struct.unpack('>I',datagram[0:4])[0]
        ip3 = ip & 255
        ip = ip >> 8
        ip2 = ip & 255
        ip = ip >> 8
        ip1 = ip & 255
        ip = ip >> 8
        ip0 = ip
        ip_adress = str.join(".",(str(ip0),str(ip1),str(ip2),str(ip3)))
        
        datagram=datagram[4:]
        Port=struct.unpack('>H',datagram[0:2])[0]
       
        datagram=datagram[2:]
        nombre_usermainroom=struct.unpack('>H',datagram[0:2])[0]
      
        datagram=datagram[2:]
        
        user_moovielist[mainroom]=id_mainroom 
        
         #parcours des utilisateurs dans la main room     
        for i in range(nombre_usermainroom) :    
            userId=struct.unpack('>H',datagram[0:2])[0]
            
            datagram=datagram[2:]
            userNameLength=struct.unpack('>H',datagram[0:2])[0]
            
            datagram=datagram[2:]
            userName=struct.unpack(str(userNameLength)+'s',datagram[0:userNameLength])[0]
            
            userName=userName.decode('utf-8') 
            datagram=datagram[userNameLength:]
            userList.append((userName,mainroom))
            userdata.append((userId,userName))
           
        
        nbre_film=struct.unpack('>H',datagram[0:2])[0]
       
        datagram=datagram[2:]
        # parcours de la liste des films pour recuperer les utilisateurs regardant un film
        for j in range(nbre_film) : 
        
            id_moovieroom=struct.unpack('>H',datagram[0:2])[0]
          
            datagram=datagram[2:]
            taille=struct.unpack('>H',datagram[0:2])[0]
            print('taille du nom de film:'+str(taille))
            datagram=datagram[2:]
     
            moovie_name=struct.unpack(str(taille)+'s',datagram[0:taille])[0]
            
            moovie_name=moovie_name.decode('utf-8') 
            datagram=datagram[taille:]
           
            # récuperer l'adresse ip et le port de chaque film
            ip=struct.unpack('>I',datagram[0:4])[0]
            ip3 = ip & 255
            ip = ip >> 8
            ip2 = ip & 255
            ip = ip >> 8
            ip1 = ip & 255
            ip = ip >> 8
            ip0 = ip
            ip_adress = str.join(".",(str(ip0),str(ip1),str(ip2),str(ip3)))
           
            datagram=datagram[4:]
            Port=struct.unpack('>H',datagram[0:2])[0]
            
            datagram=datagram[2:]
            nmbre_usermoovieroom=struct.unpack('>H',datagram[0:2])[0]
           
            datagram=datagram[2:]
            
            # recupere la liste des utilisateurs regardant un film donné
            for i in range(nmbre_usermoovieroom) :   
                userId=struct.unpack('>H',datagram[0:2])[0]
                
                datagram=datagram[2:]
                taille=struct.unpack('>H',datagram[0:2])[0]
             
                datagram=datagram[2:]
                userName=struct.unpack(str(taille)+'s',datagram[0:taille])[0]
               
                userName=userName.decode('utf-8')
                print(' user pour cette room:'+userName)
                datagram=datagram[taille:]
                userList.append((userName,moovie_name))
                userdata.append((userId,userName))
               
            liste_vide=struct.unpack('>H',datagram[0:2])[0]
            datagram=datagram[2:]
            # liste contenant le nom, port et l'ip du film
            movieList.append((moovie_name,ip,Port))
             # dictionnaire contenant les id de chaque film en fonction de leur nom
            user_moovielist[moovie_name]=id_moovieroom
        
       
        return (userList,movieList,user_moovielist,userdata)
    def message(self,Token,Seqnumber,id_user,message):
        id_user=struct.pack('>H',id_user)
        message=struct.pack('>H'+str(len(message.encode('utf−8')))+'s',len(message.encode('utf−8')),message.encode('utf−8'))
        payload=id_user+message
        msgdatasize=len(payload)
        header1=(1<<28)+(6<<24)+Token
        header2=(Seqnumber<<16)+msgdatasize
        packet=struct.pack('>II',header1,header2)+payload
        return(packet)
        
    def leaveroom(self,Token,Sequencenumber):
        
        
        header1=(1<<28)+(7<<24)+Token
        header2=(Sequencenumber<<16)+0
        packet=struct.pack('>II',header1,header2)
        return(packet)
    def sendAndWait(self,paquet,numseq,host_port):
           
        #on verifie si le nombre d'envoie est inferieur a 3 et si on a recu un ack du client
        #si non on incremente le nombre d'envoie et si oui le paquet est aquité sinon 
        #apres trois tentative on arrete d'envoyer le LRP
        if self.nombre_envoie <= 2 and self.reception_ack[numseq] == False :
            self.transport.write(paquet,host_port)
            self.nombre_envoie+=1
            print('nmbre envoielrp:'+str(self.nombre_envoie))
            reactor.callLater(1,self.sendAndWait,paquet,numseq,host_port)
        elif(self.reception_ack[numseq] == True):
           
            print('paquet aquitte')
        else:
            print('nmbre envoie:'+str(self.nombre_envoie))
            if(self.nombre_envoie > 2):
                print('paquet perdu')
    def sendLoginRequestOIE(self, userName):
        """
        :param string userName: The user name that the user has typed.

        The client proxy calls this function when the user clicks on
        the login button.
        """
        moduleLogger.debug('loginRequest called with username=%s', userName)
        print(userName)
        
        datagram=self.PaquetLRQ(1,1,0,0,0,userName)
        print(datagram)
        print(" ".join("{:02x}".format(c) for c in datagram))
        server=(self.serverAddress,self.serverPort)
        self.username=userName
        self.transport.write(datagram,server)
        self.reception_ack[self.seqnum]=False
        reactor.callLater(1,self.sendAndWait,datagram,self.seqnum,server)
    def sendChatMessageOIE(self, message):
        
        server=(self.serverAddress,self.serverPort)
       
        print('personne envoyant le message:'+str(self.userid))
        seqnumber=self.numseq(int(self.seqnum)) 
        
        datagram=self.message(self.Token,self.seqnum,self.userid,message)
        print(datagram)
        self.transport.write(datagram,server)
        self.reception_ack[self.seqnum]=False
        reactor.callLater(1,self.sendAndWait,datagram,self.seqnum,server)
        
        """
        :param message: The text of the chat message.
        :type message: string

        Called by the client proxy  when the user has decided to send
        a chat message

        .. note::
           This is the only function handling chat messages, irrespective
           of the room where the user is.  Therefore it is up to the
           c2wChatClientProctocol or to the server to make sure that this
           message is handled properly, i.e., it is shown only by the
           client(s) who are in the same room.
        """
        
        pass
    def sendJoinRoomRequestOIE(self, roomName):
        """
        :param roomName: The room name (or movie title.)

        Called by the client proxy  when the user
        has clicked on the watch button or the leave button,
        indicating that she/he wants to change room.

        .. warning:
            The controller sets roomName to
            c2w.main.constants.ROOM_IDS.MAIN_ROOM when the user
            wants to go back to the main room.
        """
        
        server=(self.serverAddress,self.serverPort)
        
        seqnumber=self.numseq(int(self.seqnum)) 
        self.seqgtr=self.seqnum
        print('seqgtr envoyé au serveur:'+str(self.seqgtr))
       
        
        datagram=self.paquetGTR(self.Token,self.seqnum,self.dictmoovie[roomName])
        print(datagram)
        self.transport.write(datagram,server)  
        self.nombre_envoie=0
        self.reception_ack[self.seqnum]=False 
        reactor.callLater(1,self.sendAndWait,datagram,self.seqnum,server)
        pass
    def sendLeaveSystemRequestOIE(self):
        """
        Called by the client proxy  when the user
        has clicked on the leave button in the main room.
        """
        server=(self.serverAddress,self.serverPort)
        
        seqnumber=self.numseq(int(self.seqnum)) 
        self.deconnexion=seqnumber+1
        print('seqgtr envoyé au serveur:'+str(self.seqgtr))
       
        
        datagram=self.leaveroom(self.Token,seqnumber+1)
        print(datagram)
        self.transport.write(datagram,server)
        self.reception_ack[self.seqnum]=False 
        reactor.callLater(1,self.sendAndWait,datagram,self.seqnum,server)   
        pass
    def datagramReceived(self, datagram, host_port):
        """
        :param string datagram: the payload of the UDP packet.
        :param host_port: a touple containing the source IP address and port.

        Called **by Twisted** when the client has received a UDP
        packet.
        """
        
        
        print('roomdata rst:'+str(datagram))
        print(" ".join("{:02x}".format(c) for c in datagram))
         #on decode le paquet recu du serveur
        (version,Type,Token,numseq,payloadsize,payload)=self.paquetsimple(datagram)
        #on numero de sequence courant recu
        self.seqnum=numseq
        self.Token=Token
   #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   #
   #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
         #si le paquet recu est ack on l'affiche
        if(Type==0):
            self.reception_ack[numseq]=True
            print('ack serveur:'+str(version)+','+str(Type)+','+str(self.Token)+','+str(self.seqnum)+','+str(payloadsize)+','+str(payload))
            if(self.seqgtr==self.seqnum):
                print('joinRoomOKONE')
                self.clientProxy.joinRoomOKONE()
                self.seqgtr=0
            elif(self.deconnexion==self.seqnum):
                self.clientProxy.leaveSystemOKONE()
                #(userList,moovieList,dictmovie)=self.depaquetageRST(datagram)
             
                
               
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
         #
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #si le paquet recu est de type login reponse on teste la valeur de coderep
         #si le paquet recu n'est pas un ack on envoie un ack au serveur
         #a revoir pour le cas ou type=2 on envoie rien
        if(Type!=0):
            print('seqnum venant du serveur:'+str(self.seqnum))
            print('le message recu est pas un ack')    
            ack=self.constructack(1,0,self.Token,self.seqnum,'')
            self.transport.write(ack,host_port)
            print('ack bien envoyé au serveur')
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
         #
         #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #si le paquet recu est de type login reponse on teste la valeur de coderep
        if(Type==2):
             #(coderep,userid,username)=struct.unpack('>BH'+str((payload)-3)+'s',payload)
            (version,Type,self.Token,self.seqnum,payloadsize,coderp,self.userid,username)=self.paquetrecuLRP(datagram)
            print('coderep:'+str(coderp))
            if(coderp==1):
               erreur='username non conforme'
               self.clientProxy.connectionRejectedONE(erreur)
           
            elif(coderp==2): 
               
               erreur='username too long'
               self.clientProxy.connectionRejectedONE(erreur)
            elif(coderp==3): 
               
               erreur='username deja utilise'
               self.clientProxy.connectionRejectedONE(erreur)
            elif(coderp==255):
               erreur='unknow error'
               self.clientProxy.connectionRejectedONE(erreur)
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #depaquetage de la userlist et de la moovielist
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if Type==4 :
            if self.seqnum==1 :
                (self.userList,self.moovieList,self.dictmoovie,self.userdata)=self.depaquetageRST(datagram)
                
                self.clientProxy.initCompleteONE(self.userList,self.moovieList)  
            elif self.seqnum>1:
                (self.userList,self.moovieList,self.dictmoovie,self.userdata)=self.depaquetageRST(datagram)
                
                self.clientProxy.setUserListONE(self.userList)
                                
     #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
     #   pour mettre a jour la liste des utilisateurs quand une nouvelle personne
     #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if(Type==6):
             (header1,header2,id_user,usernamesize,message)=struct.unpack('>IIHH'+str(len(datagram)-12)+'s',datagram)
             for user in self.userdata:
                 if(user[0]==id_user):
                     print('user envoyant le message trouvé avec id:',str(user[0]),str(user[1]))
                     
                     self.clientProxy.chatMessageReceivedONE(user[1], message.decode('utf-8')) 
             
            
             
       
        
            
     
        pass
