
//dormant state
unsigned char s_dormant[] = {0xf5, 0x2c, 0x00, 0x00, 0x00, 0x00, 0x2c, 0xf5};

//prohibit repeat, set new add mode
unsigned char s_addmode[] = {0xf5, 0x2d, 0x00, 0x01, 0x00, 0x00, 0x2c, 0xf5};

//add
unsigned char s_add1[] = {0xf5, 0x01, 0x00, 0x01, 0x01, 0x00, 0x01, 0xf5};
unsigned char s_add2[] = {0xf5, 0x02, 0x00, 0x01, 0x01, 0x00, 0x02, 0xf5};
unsigned char s_add3[] = {0xf5, 0x03, 0x00, 0x01, 0x01, 0x00, 0x03, 0xf5};

//total number of user
unsigned char s_total[] = {0xf5, 0x09, 0x00, 0x00, 0x00, 0x00, 0x09, 0xf5};
unsigned char s_compare[] = {0xf5, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x0c, 0xf5};

unsigned char s_delete_all[] = {0xf5, 0x05, 0x00, 0x00, 0x00, 0x00, 0x05, 0xf5};
unsigned char s_delete[] = {0xf5, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0xf5};

typedef union
{
  short s;
  char b[2];
}_2_bytes_to_short;


int checksum(unsigned char *s);
int select_option();
void exit_program(char * buf);
void press_enter();
void _sleep();
int ack(unsigned char q);
int ack_compare(unsigned char q);
void _write(int fd, unsigned char *cmd, unsigned char *ss);
int add_user(int fd, unsigned char * user_id);
int del_user(int fd);
int total(int fd);
int del_user_all(int fd);
