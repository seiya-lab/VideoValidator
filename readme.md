# ���挟�؃c�[��

���̃X�N���v�g�́A����t�@�C�������؂��A�L���ȓ�����W�v���邽�߂̃c�[���ł��B�܂��A�L���ȓ����WebM�`������MP4�`���ɕϊ����܂��B

## �O�����

- Python 3.6�ȏオ�C���X�g�[������Ă��邱��
- FFmpeg���V�X�e���ɃC���X�g�[������Ă��邱��

## �C���X�g�[���ƃZ�b�g�A�b�v

1. ���z�����쐬���܂��B�^�[�~�i���ňȉ��̃R�}���h�����s���܂��F

   ```shell
   conda create -n video-validator
   ```

2. �쐬�������z���ɃA�N�e�B�x�[�g���܂��F

   ```shell
   conda activate video-validator
   ```

3. �K�v�ȃ��C�u�������C���X�g�[�����܂��F

   ```shell
   conda install pip
   pip install opencv-python
   ```

## �t�@�C���\��

```
Videovalidator.py
README.md
```

- `Videovalidator.py`: ���挟�؃c�[���̃��C���X�N���v�g�ł��B
- `README.md`: ���̐����t�@�C���ł��B

```
root/
������ VideoValidator/
��   ������ videovalidator.py
��   ������ README.md
������ data/
��   ������ ���[�UID1/
��   ��   ������ ����ID1.webm
��   ��   ������ ����ID2.webm
��   ��   ������ ...
��   ������ ���[�UID2/
��   ��   ������ ����ID1.webm
��   ��   ������ ...
��   ������ ...
������ processed_data/
    ������ ���[�UID1/
    ��   ������ ����ID1.mp4
    ��   ������ ����ID2.mp4
    ��   ������ ...
    ������ ���[�UID2/
    ��   ������ ����ID1.mp4
    ��   ������ ...
    ������ ...
```

- `VideoValidator/`: �v���W�F�N�g�̃��[�g�f�B���N�g���ł��B���̃f�B���N�g���� "VideoValidator" �Ƃ������O�ł���A�v���W�F�N�g�̃t�@�C�����i�[����܂��B
- `VideoValidator/videovalidator.py`: ���挟�؃c�[���̃��C���X�N���v�g�ł��B���̃X�N���v�g�� "VideoValidator" �f�B���N�g�����ɔz�u���Ă��������B
- `VideoValidator/README.md`: ���̐����t�@�C���ł��B���l�� "VideoValidator" �f�B���N�g�����ɔz�u���Ă��������B
- `data/`: ���͂ƂȂ铮��t�@�C�����i�[�����f�B���N�g���ł��B"VideoValidator" �f�B���N�g���Ɠ����K�w�ɂ���܂��B�e���[�U���ƂɃT�u�f�B���N�g�����쐬����A���̒��ɓ���t�@�C�����z�u����܂��B
- `processed_data/`: �ϊ���̓���t�@�C�����i�[�����f�B���N�g���ł��B���l�� "VideoValidator" �f�B���N�g���Ɠ����K�w�ɂ���܂��B���̓f�B���N�g���Ɠ��l�ɁA�e���[�U���ƂɃT�u�f�B���N�g�����쐬����A���̒��ɕϊ���̓���t�@�C�����z�u����܂��B

���̃f�B���N�g���\���ɏ]���āA"VideoValidator" �f�B���N�g�����ɃX�N���v�g�t�@�C�� `videovalidator.py` �Ɛ����t�@�C�� `README.md` ��z�u���Ă��������B�܂��A���͓���t�@�C���� `data/` �f�B���N�g���ɁA�ϊ���̓���t�@�C���� `processed_data/` �f�B���N�g���ɔz�u���Ă��������B

## �g�p�@

1. `Videovalidator.py` �X�N���v�g���J���܂��B
2. `DATA_DIR` �ϐ���K�؂ȃf�[�^�f�B���N�g���̃p�X�ɐݒ肵�܂��B�f�[�^�f�B���N�g���́A���[�U���ƂɃT�u�f�B���N�g�����쐬����A�e�T�u�f�B���N�g�����ɓ���t�@�C�����i�[����Ă���z��ł��B
3. `PROCESSED_DATA_DIR` �ϐ���ϊ���̓�����i�[����f�B���N�g���̃p�X�ɐݒ肵�܂��B���̃f�B���N�g���͎��O�ɍ쐬���Ă����K�v������܂��B
4. ���̑��̒萔��K�v�ɉ����ĕύX���܂��i�𑜓x�A�t�@�C���T�C�Y�����Ȃǁj�B
5. �^�[�~�i���ňȉ��̃R�}���h�����s���āA�X�N���v�g�����s���܂��F

   ```shell
   python Videovalidator.py
   ```

6. �X�N���v�g�̓f�[�^�f�B���N�g�����̊e���[�U�̓�������؂��A�L���ȓ����ϊ����A���t���Ƃɓ���̑����v���Ԃ��o�͂��܂��B

## ���C�Z���X

MIT���C�Z���X�̂��ƂŌ��J����Ă��܂��B�ڍׂɂ��ẮA[LICENSE](LICENSE) �t�@�C�����Q�Ƃ��Ă��������B