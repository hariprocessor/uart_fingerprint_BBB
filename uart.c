/*
 * Filename: uart.c
 * Version : 1.0
 * 
 * Project : Embedded Software (Fingerprint Stamp)
 * Author  : Haryeong Kim
 * Contact : hariprocessor@gmail.com
 * Date    : 25 May 2015
 */

#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <time.h>
#include <termios.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <string.h>
#include "protocol.h"
#define BONEPATH "/sys/devices/bone_capemgr.9/slots"

int
main(int argc, char *argv[])
{

  int input;
  int i, j, fd;
  FILE *uart;
  char buf[30] = "/dev/tty";
  int temp;
  struct termios uart1, old;
  unsigned char ss[8] = {0,};
  unsigned char user_id[2] = {0x00, 0x01};

  uart = fopen(BONEPATH, "w");
  if(uart == NULL) printf("slots didn't open\n");
  fseek(uart,0,SEEK_SET);

  fprintf(uart, "BB-UART5");
  strcat(buf, "O4");

  fflush(uart);
  fclose(uart);

  fd = open(buf, O_RDWR | O_NOCTTY);
  if(fd < 0) printf("port failed to open\n");

  tcgetattr(fd,&old);
  bzero(&uart1,sizeof(uart1)); 

  uart1.c_cflag = B19200 | CS8 | CLOCAL | CREAD;
  uart1.c_iflag = IGNPAR | ICRNL;
  uart1.c_oflag = 0;
  uart1.c_lflag = 0;

  uart1.c_cc[VTIME] = 0;
  uart1.c_cc[VMIN]  = 1;

  tcflush(fd,TCIFLUSH);
  tcsetattr(fd,TCSANOW,&uart1);

  _write(fd, s_delete_all, ss);

  while(1)
    {
      input = select_option();
      switch(input){
      case 1:
	if(add_user(fd, user_id) == 0)
	  {
	    if(user_id[1] == 0xff) 
	      {
		user_id[0]++;
		user_id[1] = 0x00;
	      }
	    else
	      user_id[1]++;
	  }
	break;
      case 2:
	del_user(fd);
	break;
      case 3:
	del_user_all(fd);
	break;
      case 4:
	total(fd);
	break;
      case 5:
	close(fd);
	exit(0);
      default:
	break;
      }
    }


  close(fd);

  return 0;
}

int
checksum(unsigned char *s)
{
  return s[1]^s[2]^s[3]^s[4]^s[5];
}

int
select_option()
{
  int input;
  system("clear");
  printf("+----------------------------------+\n");
  printf("|             FINGERPRINT          |\n");
  printf("| 1. Add user                      |\n");
  printf("| 2. Delete user                   |\n");
  printf("| 3. Delete all user               |\n");
  printf("| 4. Show total number of user     |\n");
  printf("| 5. Exit program                  |\n");
  printf("+----------------------------------+\n");
  printf("\n Select the number : ");
  scanf("%d", &input);
  return input;
}

void
exit_program(char * buf)
{
  printf("%s\n", buf);
  exit(0);
}

void
press_enter()
{
  printf("Press enter key to continue...\n");
  char prev = 0;
  while(1)
    {
      char c = getchar();
      if(c == '\n' && prev == c)
	break;
      prev = c; 
    }
}
void
_sleep()
{
  usleep(1000 * 1600);
}
int
ack(unsigned char q)
{
  switch(q)
    {
    case 0x00:
      return 0;
    case 0x01:
      printf("Request was failed.\n");
      return -1;
    case 0x04:
      printf("Database is full.\n");
      return -1;
    case 0x05:
      printf("There is no user.\n");
      return -1;
    case 0x07:
      printf("There is already user.\n");
      return -1;
    case 0x08:
      printf("Aquisition timeout.\n");
      return -1;
    default:
      printf("Unknown error.\n");
      return -1;
    }
}

int
ack_compare(unsigned char q)
{
  switch(q)
    {
    case 0x05:
      printf("There is no user.\n");
      return -1;
    case 0x08:
      printf("Aquisition timeout.\n");
      return -1;
    case 0x01:
      return 0;
    case 0x02:
      return 0;
    case 0x03:
      return 0;
    default:
      printf("Unknown error.\n");
      return -1;

    }
}

void
_write(int fd, unsigned char *cmd, unsigned char *ss)
{
  int i, size = 0, size_t = 0;
  unsigned char tmp[8];
  fsync(fd);
  write(fd, cmd, 8);
  while(size != 8)
    {
      size_t = read(fd, tmp, 8);
      for(i = 0; i < size_t; i++)
	ss[size+i] = tmp[i];
      size += size_t;
    }
}


int
add_user(int fd, unsigned char * user_id)
{
  char c;
  int i;
  unsigned char ss[8] = {0,};

  printf("user id : %2x%2x\n", user_id[0], user_id[1]);
  s_add1[2] = user_id[0];
  s_add1[3] = user_id[1];
  s_add1[6] = checksum(s_add1);
  s_add2[2] = user_id[0];
  s_add2[3] = user_id[1];
  s_add2[6] = checksum(s_add2);
  s_add3[2] = user_id[0];
  s_add3[3] = user_id[1];
  s_add3[6] = checksum(s_add3);
    
  _write(fd, s_addmode, ss);
  if(ack(ss[4]) == -1)
    {
      press_enter();
      return -1;
    }

  _write(fd, s_add1, ss);
  if(ack(ss[4]) == -1)
    {
      press_enter();
      return -1;
    }

  _write(fd, s_add2, ss);
  if(ack(ss[4]) == -1)
    {
      press_enter();
      return -1;
    }

  _write(fd, s_add3, ss);
  if(ack(ss[4]) == -1)
    {
      press_enter();
      return -1;
    }

  printf("Fingerprint added!\n");
  press_enter();
  return 0;
}

int
del_user(int fd)
{
  int i;
  unsigned char ss[8] = {0,};
  int user_id[2];

  _write(fd, s_compare, ss);

  if(ack_compare(ss[4]) == -1)
    {
      press_enter();
      return -1;
    }

  user_id[0] = ss[2];
  user_id[1] = ss[3];

  printf("user id : %2x%2x\n", user_id[0], user_id[1]);
  s_delete[2] = user_id[0];
  s_delete[3] = user_id[1];
  s_delete[6] = checksum(s_delete);

  _write(fd, s_delete, ss);
  if(ack(ss[4]) == -1)
    {
      press_enter();
      return -1;
    }

  press_enter();
  return 0;
}


int
total(int fd)
{
  _2_bytes_to_short u;
  int i;
  unsigned char ss[8] = {0,};
  _write(fd, s_total, ss);
  if(ack(ss[4]) == -1)
    {
      press_enter();
      return -1;
    }
  u.b[0] = ss[3];
  u.b[1] = ss[2];
  printf("Total number of user : %d\n", u.s);
  press_enter();
  return 0;
}

int
del_user_all(int fd)
{
  int i;
  unsigned char ss[8] = {0,};
  int user_id[2];

  _write(fd, s_delete_all, ss);
  if(ack(ss[4]) == -1)
    {
      press_enter();
      return -1;
    }

  printf("Delete user all! \n");
  press_enter();
  return 0;
}
