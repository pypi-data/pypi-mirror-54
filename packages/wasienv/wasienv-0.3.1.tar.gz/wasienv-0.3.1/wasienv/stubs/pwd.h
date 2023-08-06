#ifndef _PWD_H
#define _PWD_H

#ifdef __cplusplus
extern "C" {
#endif

#include <features.h>

#define __NEED_size_t
#define __NEED_uid_t
#define __NEED_gid_t

#ifdef _GNU_SOURCE
#define __NEED_FILE
#endif

#include <bits/alltypes.h>

struct passwd
{
	char *pw_name;
	char *pw_passwd;
	uid_t pw_uid;
	gid_t pw_gid;
	char *pw_gecos;
	char *pw_dir;
	char *pw_shell;
};

void setpwent (void);
void endpwent (void);
struct passwd *getpwent (void);

struct passwd *getpwuid (uid_t);
struct passwd *getpwnam (const char *);
int getpwuid_r (uid_t, struct passwd *, char *, size_t, struct passwd **);
int getpwnam_r (const char *, struct passwd *, char *, size_t, struct passwd **);

#ifdef _GNU_SOURCE
struct passwd *fgetpwent(FILE *);
int putpwent(const struct passwd *, FILE *);
#endif

#endif

// Stub implementations
__attribute__((weak)) void setpwent (void) { }
__attribute__((weak)) void endpwent (void) { }
__attribute__((weak)) struct passwd *getpwent (void) { return 0; }
__attribute__((weak)) struct passwd *getpwuid (uid_t unused) { return 0; }
__attribute__((weak)) struct passwd *getpwnam (const char * unused) { return 0; }
__attribute__((weak)) int getpwuid_r (uid_t unused1, struct passwd * unused2, char * unused3, size_t unused4, struct passwd ** unused5) { return 0; }
__attribute__((weak)) int getpwnam_r (const char * unused1, struct passwd * unused2, char * unused3, size_t unused4, struct passwd ** unused5) { return 0; }


#ifdef _GNU_SOURCE
__attribute__((weak)) struct passwd *fgetpwent(FILE * unused1) { return 0; }
__attribute__((weak)) int putpwent(const struct passwd * unused1, FILE * unused2) { return 0; }
#endif

#ifdef __cplusplus
}
#endif
