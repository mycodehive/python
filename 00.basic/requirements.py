import pkg_resources

# 설치된 패키지 목록 가져오기
installed_packages = pkg_resources.working_set
requirements = "\n".join(f"{pkg.key}=={pkg.version}" for pkg in installed_packages)

# requirements.txt로 저장
with open("requirements.txt", "w") as f:
    f.write(requirements)

print("requirements.txt 파일이 생성되었습니다.")
