import org.example.test.Main;
import org.example.test.api.UserApi;
import org.example.test.invoker.ApiException;
import org.example.test.model.User;
import org.junit.jupiter.api.*;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class UserTest {

    UserApi userApi = new UserApi();

    @Test
    @Order(1)
    public void createUserTest() throws ApiException {
    User user = userApi.createUser(new User().name("test"));
    assertEquals("test", user.getName());
    }

    @Test
    @Order(2)
    public void createExistingUserTest() throws ApiException {
        assertThrows(ApiException.class, () -> userApi.createUser(new User().name("test")));
    }

    @Test
    @Order(3)
    public void getUserTest() throws ApiException {
        User user = userApi.getUsers("test", null, null).get(0);
        assertEquals("test", user.getName());
        user = userApi.getUser(user.getId());
        assertEquals("test", user.getName());
    }

    @Test
    @Order(4)
    public void getUsersTest() throws ApiException {
        for(int i = 0; i < 20; i++) {
            userApi.createUser(new User().name("test" + i));
        }
        int firstTestUser = userApi.getUsers("test1", null, null).get(0).getId();
        List<User> users = userApi.getUsers(null, firstTestUser, 2);
        assertEquals(2, users.size());
        assertEquals("test2", users.get(0).getName());
        assertEquals("test3", users.get(1).getName());
    }

    @Test
    @Order(4)
    public void changeUsernameTest() throws ApiException {
        User user = userApi.getUsers("test", null, null).get(0);
        user = userApi.updateUser(user.getId(), user.name("testtest"));
        assertEquals("testtest", user.getName());
        User user2 = userApi.getUsers("testtest", null, null).get(0);
        assertEquals("testtest", user2.getName());
        assertEquals(user2, user);
        user = userApi.updateUser(user.getId(), user.name("test"));
        assertEquals("test", user.getName());
    }

    @Test
    @Order(5)
    public void addPictureToUser() throws ApiException, FileNotFoundException {
        User user = userApi.getUsers("test", null, null).get(0);
        userApi.addPictureToUser(user.getId(), getPicture());
    }

    @Test
    @Order(6)
    public void deleteUsers() throws ApiException {
        int firstTestUser = userApi.getUsers("test", null, null).get(0).getId();
        for(int i = firstTestUser; i <= firstTestUser + 20; i++) {
            userApi.deleteUser(i);
        }
    }

    public static File getPicture() throws FileNotFoundException {
        ClassLoader classLoader = Main.class.getClassLoader();
        File picture = new File(classLoader.getResource("logo.png").getFile());
        if(picture.isFile()) {
            System.out.println("Loaded valid picture");
            return picture;
        } else {
            throw new FileNotFoundException("Picture not found");
        }
    }
}
