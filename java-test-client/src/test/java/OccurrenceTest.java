import org.example.test.Main;
import org.example.test.api.BirdApi;
import org.example.test.api.OccurrenceApi;
import org.example.test.api.UserApi;
import org.example.test.invoker.ApiException;
import org.example.test.model.Bird;
import org.example.test.model.Occurrence;
import org.example.test.model.User;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;

import java.io.File;
import java.io.FileNotFoundException;
import java.time.OffsetDateTime;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class OccurrenceTest {

    OccurrenceApi occurrenceApi = new OccurrenceApi();
    UserApi userApi = new UserApi();
    BirdApi birdApi = new BirdApi();
    int firstOccurence;

    @Test
    @Order(1)
    public void createOccurenceTest() throws ApiException {
        User user = userApi.createUser(new User().name("test"));
        Bird bird = birdApi.getBird(1);
        OffsetDateTime time = OffsetDateTime.now();
        Occurrence occurrence = occurrenceApi.addOccurrence(new Occurrence().userId(user.getId()).birdId(bird.getId()).latitude(42.0).longitude(42.0).altitude(42.0).note("lol").timestamp(time));
        firstOccurence = occurrence.getId();
        assertEquals(user.getId(), occurrence.getUser().getId());
        assertEquals(user.getName(), occurrence.getUser().getName());
        assertEquals(bird.getId(), occurrence.getBird().getId());
        assertEquals(bird.getPictureUrl(), occurrence.getBird().getPictureUrl());
        assertEquals(bird.getBreeding(), occurrence.getBird().getBreeding());
        assertEquals(bird.getAuthority(), occurrence.getBird().getAuthority());
        assertEquals(bird.getShape(), occurrence.getBird().getShape());
        assertEquals(bird.getSize(), occurrence.getBird().getSize());
        assertEquals(bird.getFamily(), occurrence.getBird().getFamily());
        assertEquals(bird.getSpecies(), occurrence.getBird().getSpecies());
        assertEquals(bird.getSubregion(), occurrence.getBird().getSubregion());
        assertEquals(user.getId(), occurrence.getUserId());
        assertEquals(bird.getId(), occurrence.getBirdId());
        assertEquals(42.0, occurrence.getLongitude());
        assertEquals(42.0, occurrence.getAltitude());
        assertEquals(42.0, occurrence.getLatitude());
        assertEquals("lol", occurrence.getNote());
        //assertEquals(time, occurrence.getTimestamp()); //TODO Try PostgreSQL
    }

    @Test
    @Order(2)
    public void checkOccurenceInBirdTest() throws ApiException {
        User user = userApi.getUsers("test", null, null).get(0);
        Occurrence occurrence = occurrenceApi.addOccurrence(new Occurrence().userId(user.getId()).birdId(1).latitude(42.0).longitude(42.0).altitude(42.0).note("lol"));
        Bird bird = birdApi.getBird(1);
        assertTrue(bird.getOccurrences().contains(occurrence));
    }

    @Test
    @Order(3)
    public void checkOccurenceInUserTest() throws ApiException {
        User user = userApi.getUsers("test", null, null).get(0);
        Occurrence occurrence = occurrenceApi.addOccurrence(new Occurrence().userId(user.getId()).birdId(1).latitude(42.0).longitude(42.0).altitude(42.0).note("lol"));
        user = userApi.getUser(user.getId());
        assertTrue(user.getBirdOccurrences().contains(occurrence));
    }

    @Test
    @Order(4)
    public void updateOccurenceTest() throws ApiException {
        User user = userApi.getUsers("test", null, null).get(0);
        Occurrence occurrence = occurrenceApi.getOccurrences(user.getId(), 1, null, null, null, null, null, null).get(0);
        occurrence.setNote("abc");
        occurrence.setAltitude(20.0);
        occurrence.setLongitude(10.0);
        occurrence.setLatitude(10.0);
        occurrence.setBirdId(3);
        occurrence = occurrenceApi.updateOccurrence(occurrence.getId(), occurrence);
        assertEquals(user.getId(), occurrence.getUser().getId());
        assertEquals("test", occurrence.getUser().getName());
        assertEquals(3, occurrence.getBird().getId());
        assertEquals(10.0, occurrence.getLongitude());
        assertEquals(20.0, occurrence.getAltitude());
        assertEquals(10.0, occurrence.getLatitude());
        assertEquals("abc", occurrence.getNote());
        //assertEquals(time, occurrence.getTimestamp()); //TODO Try PostgreSQL
    }

    @Test
    @Order(4)
    public void queryOccurenceTest() throws ApiException {
        // Todo
    }

    @Test
    @Order(5)
    public void deleteOccurenceTest() throws ApiException, FileNotFoundException {
        boolean deleting = true;
        while (deleting)
            try {
                occurrenceApi.getOccurrence(firstOccurence);
                occurrenceApi.deleteOccurrence(firstOccurence);
                firstOccurence++;
            } catch (ApiException e) {
                deleting = false;
            }
        userApi.deleteUser(userApi.getUsers("test", null, null).get(0).getId());
    }
}
