# SVU exam time TUI
a lightweight TUI (Terminal User Interface) for rightfully paranoid syrian Virtual university students to see how much time do they have until every exam starts in thier calender, automatically updating for it to work in the background
# install instructions
1. **clone the repository**
- execute:
```bash
git clone https://github.com/abdullahaldarwish/SVUexamtimeTUI.git
cd SVUexamtimeTUI
```
2. **copy the table HTML from your browers to `exams.html`**
   - first method (recommended):
        create `exams.html` in the project directory and copy-paste the table HTML from the browser to `exams.html`
   - second method:
        skip this step temporarily and continue to the next steps
3. **Verify Python is installed**
```bash
python --version
```
(or `python3 --version` on some systems)
4. **Install dependencies**
```bash
pip install -r requirements.txt
```
# running the app
- you can run the script by executing `python script.py` and this will use the default parameter(s)
- if you skipped copying the exams table; the app will prompt you to paste it in the terminal
- you can specify how much time it takes to refresh by adding the argument `--interval` or `-i` followed by the duration **default is 5 minutes and minimum is 50 seconds** 
    duration is specified by a number then a period, for example: 5m is 5 minutes
    periods are:
    - s -> seconds
    - m -> minute(s)
    - h -> hour(s)
    - d -> day(s)
- example: `python script.py --interval 2h` will refresh every 2 hours