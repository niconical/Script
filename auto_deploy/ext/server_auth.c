#include <arpa/inet.h>
#include <cpuid.h>
#include <net/if.h>
#include <net/if_arp.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/socket.h>

#include <ifaddrs.h>
#include <sys/types.h>

char *FILE_DIR = "./DEVICE_INFO";

static char *get_cpuid() {
  unsigned int eax, ebx, ecx, edx;
  char id[32];
  int n;

  if (0 == __get_cpuid(1, &eax, &ebx, &ecx, &edx)) {
    return NULL;
  }

  n = snprintf(id, sizeof(id), "%08X%08X", htonl(eax), htonl(edx));

  return strdup(id);
}

static char *get_macaddr(char *eth_name) {
  int sock;
  struct sockaddr_in sin;
  struct sockaddr sa;
  struct ifreq ifr;
  unsigned char mac[6];
  char macstr[32];
  int n;

  sock = socket(AF_INET, SOCK_DGRAM, 0);
  if (sock == -1) {
    perror("socket");
    return NULL;
  }

  strncpy(ifr.ifr_name, eth_name, IFNAMSIZ);
  ifr.ifr_name[IFNAMSIZ - 1] = 0;

  memset(mac, 0, sizeof(mac));
  if (ioctl(sock, SIOCGIFHWADDR, &ifr) < 0) {
    return NULL;
  }

  memcpy(&sa, &ifr.ifr_addr, sizeof(sin));
  memcpy(mac, sa.sa_data, sizeof(mac));

  int i;
  for (i = 0; i < sizeof(mac) / sizeof(mac[0]); ++i) {
    if (mac[i] != 0) {
      break;
    }
  }
  if (i == sizeof(mac) / sizeof(mac[0])) {
    return NULL;
  }
  n = snprintf(macstr, sizeof(macstr), "%.2X:%.2X:%.2X:%.2X:%.2X:%.2X", mac[0],
               mac[1], mac[2], mac[3], mac[4], mac[5]);

  return strdup(macstr);
}

int main() {
  char *cpuid = get_cpuid();
  struct ifaddrs *ifaddr, *ifa;
  FILE *fp = NULL;
  fp = fopen(FILE_DIR, "w+");
  if (getifaddrs(&ifaddr) == 0) {
    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
      char *m = get_macaddr(ifa->ifa_name);
      if (ifa->ifa_addr->sa_family == AF_INET && m) {
        fprintf(fp, "MAC: %s\n", m ? m : "NO");
      }
      free(m);
    }
    freeifaddrs(ifaddr);
    fprintf(fp, "CPU: %s\n", cpuid ? cpuid : "NO");
    free(cpuid);
  }
}
