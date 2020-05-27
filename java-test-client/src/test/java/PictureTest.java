import org.example.test.api.BirdApi;
import org.example.test.api.FamilyApi;
import org.example.test.api.PicturesApi;
import org.example.test.invoker.ApiClient;
import org.example.test.invoker.ApiException;
import org.example.test.model.Family;
import org.junit.jupiter.api.Test;

import java.io.File;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class PictureTest {
    PicturesApi picturesApi = new PicturesApi();

    @Test
    public void getCuculidaeFamily() throws ApiException {
        File file = picturesApi.getPictureByFilepath(new BirdApi().getBird(1).getPictureUrl());
        assertTrue(file.exists());
    }
}
