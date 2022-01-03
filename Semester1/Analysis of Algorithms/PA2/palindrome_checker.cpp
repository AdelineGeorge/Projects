#include <cstdio>
#include <cstdlib>
#include <cstring>

using namespace std;

char s[2010], pal[2010];
int n, len, len1;

int main(int argc, char* argv[]){
	if (argc != 4){
		printf("usage: %s inputfile standardoutputfile youroutputfile\n", argv[0]);
		return 0;
	}
	FILE *fp;
	
	fp = fopen(argv[1], "r");
	fscanf(fp, "%s\n", s);
	fclose(fp);
	n = strlen(s);

	fp = fopen(argv[2], "r");
	fscanf(fp, "%d", &len);
	fclose(fp);

	fp = fopen(argv[3], "r");
	fscanf(fp, "%d\n", &len1);
	fscanf(fp, "%s\n", pal);
	fclose(fp);

	if (len!=len1) {
		printf("0 The length of the longest palindrome is not correct.\n");
		return 0;
	}
	if (strlen(pal)!=len) {
		printf("0 The lengthes do not match.\n");
		return 0;
	}
	int i, j;
	for (i = 0; i < len/2; i++) 
		if (pal[i]!=pal[len-1-i]) {
			printf("0 The string you output is not a palindrome.\n");
			return 0;
		}
	j = 0;
	for (i = 0; i < len; i++) {
		while (j < n && s[j]!=pal[i]) j++;
		if (j >= n){
			printf("0 The palindrome you output is not a subsequence of the input string.\n");
			return 0;
		}
		j++;
	}
	printf("1 Correct.\n");
}

