import org.example.test.api.BirdApi;
import org.example.test.invoker.ApiException;
import org.example.test.model.Bird;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class BirdTest {

    BirdApi birdApi = new BirdApi();

    @Test
    public void getBirds() throws ApiException {
        List<Bird> birds = birdApi.getBirds(null, null, null, null, null, null, null);
        assertEquals(20, birds.size());
    }

    @Test
    public void getBirdsByShape() throws ApiException {
        List<Bird> birds = birdApi.getBirds(null, null, null, Bird.ShapeEnum.CHICKEN_LIKE.toString(), null, null, null);
        birds.forEach(bird -> assertEquals(bird.getShape(), Bird.ShapeEnum.CHICKEN_LIKE));
    }

    @Test
    public void getBirdsByBreeding() throws ApiException {
        List<Bird> birds = birdApi.getBirds(null, null, null, null, Bird.BreedingEnum.EU.toString(), null, null);
        birds.forEach(bird -> assertEquals(bird.getBreeding(), Bird.BreedingEnum.EU));
    }
}
