c This file was written by the init.sh script.  Change that, not this.

      call aampp
      end

      subroutine init0(stdin,stdout,stderr,intsize,realsize,wordsize,
     &system)
      integer stdin,stdout,stderr,intsize,realsize,wordsize
      character *(*) system
      stdin = 5
      stdout = 6
      stderr = 0
      intsize = 4
      realsize = 4
      wordsize = 32
      system = "LINUX"
      end
