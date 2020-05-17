from pathlib import Path

from fastapi import HTTPException, File

async def uploadPicture(picture: File, path: Path, override: bool = False):

    if (not path.exists()) or override:
        content = await picture.read()

        try:
            with path.open('wb') as target_file:
                target_file.write(content)

        except FileNotFoundError as error:
            raise HTTPException(status_code=404, detail='{}'.format(error))
        
    else:
        raise HTTPException(status_code=409, detail='File already exists')

    return path