■ 생성된 파일을 ffmpeg로 따로 Merge하는 명령어
<pre><code>
ffmpeg -i downloaded_video_1080p.f137.mp4 -i downloaded_video_1080p.f140.m4a -c:v copy -c:a aac -b:a 192k merged_output.mp4
</code></pre>

■ ffmpeg 다운로드
1. 공식 FFmpeg 웹사이트(https://ffmpeg.org/download.html)로 이동합니다.
2. Windows 버전을 다운로드하기 위해 링크 이동: FFmpeg builds: https://www.gyan.dev/ffmpeg/builds/
3. git master builds > "ffmpeg-release-essentials.zip" 파일을 다운로드합니다.
4. 설치된 경로 체크하기

■ ffmpeg 환경 변수 설정
1. ffmpeg 명령어를 어디서든 실행할 수 있도록 시스템 PATH에 추가합니다.
2. 시작 메뉴에서 환경 변수를 검색하고 **"시스템 환경 변수 편집"**을 클릭합니다.
3. 시스템 속성 창이 열리면, "고급" 탭에서 "환경 변수" 버튼을 클릭합니다.
4. "환경 변수" 창에서 "Path" 항목을 선택하고 "편집" 버튼을 클릭합니다.
5. **"새로 만들기"**를 클릭하고 ffmpeg의 bin 폴더 경로를 입력합니다

■ ffmpeg 설치 확인
<pre><code>
ffmpeg -version
</code></pre>
